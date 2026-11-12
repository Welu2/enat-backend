"""Separate process entrypoints: python -m app.jobs scheduler|worker|status|replay."""

import argparse
import json
import logging
import signal
from datetime import date
from threading import Event, Thread
from time import monotonic
from uuid import UUID, uuid4

from app.core import observability
from app.db import jobs
from app.db.data import transaction
from app.db.repositories.reminders import ReminderRepository
from app.db.worker import close_pool, worker_context
from app.services.reminders import ReminderService

logger = logging.getLogger("enat.jobs")


def handle(job):
    if job["kind"] == "user.daily":
        ReminderService().run_user_day(
            job["user_id"], date.fromisoformat(job["payload"]["occurrence"])
        )
    elif job["kind"] == "outbox.deliver":
        # Delivery means a durable in-app notification, not unconfigured push/SMS.
        with transaction() as conn:
            event = conn.execute(
                "SELECT * FROM domain_outbox WHERE id=%s AND user_id=%s FOR UPDATE",
                (job["payload"]["outbox_id"], job["user_id"]),
            ).fetchone()
            if event is None:
                raise ValueError("Missing outbox event")
            if event["delivered_at"] is not None:
                return
            messages = {
                "checkin.completed": "Your check-in was saved.",
                "summary.created": "Your clinical summary is ready.",
            }
            if event["event_type"] not in messages:
                raise ValueError("Unsupported outbox event")
            # A disabled account gets no new notification; retain delivery evidence.
            from app.db.repositories.users import UserRepository

            if UserRepository().get_by_id(job["user_id"]):
                ReminderRepository().create_once(
                    job["user_id"],
                    event["event_type"],
                    messages[event["event_type"]],
                    event["created_at"],
                    "outbox:" + str(event["id"]),
                )
            conn.execute(
                "UPDATE domain_outbox SET delivered_at=now() WHERE id=%s",
                (event["id"],),
            )
    else:
        raise ValueError("Unsupported job")


def process_one():
    with worker_context():
        job = jobs.claim()
    if job is None:
        return False
    stop = Event()

    def renew():
        while not stop.wait(15):
            try:
                with worker_context():
                    if not jobs.heartbeat(job):
                        return
            except Exception:
                logger.warning("job_heartbeat_failed", extra={"job_id": str(job["id"])})
                return

    heartbeat = Thread(target=renew, daemon=True)
    heartbeat.start()
    try:
        with (
            worker_context(job["user_id"]),
            observability.span(
                "job." + job["kind"], parent=job["payload"].get("_traceparent")
            ),
        ):
            handle(job)
            jobs.finish(job)
            logger.info("job_completed", extra={"job_id": str(job["id"])})
    except Exception:
        # Never persist exception text: it may include patient/provider payloads.
        logger.warning("job_handler_failed", extra={"job_id": str(job["id"])})
        with worker_context():
            jobs.fail(job)
    finally:
        stop.set()
        heartbeat.join(timeout=10)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["scheduler", "worker", "status", "replay"])
    parser.add_argument("--job-id", type=UUID)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    from app.config import get_settings

    observability.configure(get_settings())

    if get_settings().process_role != "worker":
        parser.error("Set PROCESS_ROLE=worker for job commands")
    if args.command == "replay" and not args.job_id:
        parser.error("replay requires --job-id")
    stop, token = Event(), uuid4()
    last_cleanup = 0.0
    last_metrics = 0.0
    from app.core import worker_metrics

    exporter = (
        worker_metrics.start(get_settings().metrics_token)
        if args.command in {"worker", "scheduler"} and not args.once
        else None
    )
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    try:
        while not stop.is_set():
            try:
                with worker_context():
                    if monotonic() - last_metrics >= 30:
                        worker_metrics.update()
                        last_metrics = monotonic()
                    if args.command == "status":
                        print(json.dumps(jobs.stats(), default=str))
                        return
                    if args.command == "replay":
                        print(json.dumps({"replayed": jobs.replay(args.job_id)}))
                        return
                    if args.command == "scheduler":
                        if monotonic() - last_cleanup >= 60:
                            with transaction() as conn:
                                conn.execute("SELECT enat_cleanup_security_state()")
                            last_cleanup = monotonic()
                        busy = jobs.schedule_page(token) > 0
                        busy = jobs.dispatch_outbox() > 0 or busy
                    else:
                        busy = process_one()
            except Exception:
                logger.error("job_process_temporarily_unavailable")
                if args.once or args.command in ("status", "replay"):
                    raise SystemExit(
                        "Job command unavailable; inspect protected operational state"
                    ) from None
                busy = False
            if args.once:
                break
            stop.wait(0.1 if busy else 5)
    finally:
        if exporter:
            exporter.shutdown()
            exporter.server_close()
        observability.shutdown()
        close_pool()


if __name__ == "__main__":
    main()
