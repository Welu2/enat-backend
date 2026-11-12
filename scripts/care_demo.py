"""Seed and verify a care/offline demo only in test_database.py's disposable cluster."""

import json
import os
import sys
from pathlib import Path
from uuid import UUID, uuid4

import psycopg


def main():
    dsn = os.environ.get("ENAT_TEST_ADMIN_DSN", "")
    directory = psycopg.conninfo.conninfo_to_dict(dsn).get("host", "")
    if not directory.startswith("/tmp/enat-security-"):
        raise SystemExit("Only disposable test_database.py clusters are supported")
    os.environ.update(
        {
            "ENVIRONMENT": "test",
            "PROCESS_ROLE": "api",
            "DATABASE_URL": os.environ["ENAT_TEST_APP_DSN"],
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "synthetic-placeholder",
            "ADDIS_API_KEY": "synthetic-placeholder",
            "ENABLE_CARE_PORTAL": "true",
            "ENABLE_OFFLINE_CHECKINS": "true",
            "ENABLE_REQUEST_LIMITS": "false",
            "ENABLE_PRIVACY_TOOLS": "false",
            "ENABLE_DEV_ROUTES": "false",
            "ENABLE_EMBEDDED_SCHEDULER": "false",
            "LEGACY_HS256_UNTIL": "",
        }
    )
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from app.core.clock import utc_now
    from app.core.errors import NotFound
    from app.db import data
    from app.models.care import CareInviteRequest
    from app.models.offline_checkin import OfflineCheckInRequest
    from app.services import care_access, offline_checkin, portal

    users = {
        kind: data.resolve_identity(
            "supabase", str(uuid4()), f"{kind}@synthetic.invalid"
        )
        for kind in ("patient", "clinician", "trusted")
    }
    with psycopg.connect(dsn) as conn:
        conn.execute(
            "INSERT INTO clinician_profiles(user_id,display_name) VALUES(%s,'Demo clinician')",
            (users["clinician"]["id"],),
        )
    invitations = {}
    for kind, relation in (("clinician", "clinician"), ("trusted", "trusted_person")):
        data.current_user_id.set(users["patient"]["id"])
        invite = care_access.invite(
            CareInviteRequest(
                recipient_id=users[kind]["id"], relationship=relation, consent=True
            )
        )
        data.current_user_id.set(users[kind]["id"])
        invitations[kind] = care_access.accept(invite["token"])
    data.current_user_id.set(users["patient"]["id"])
    now = utc_now()
    request = OfflineCheckInRequest(
        schema_version=1,
        client_submission_id=uuid4(),
        recorded_at=now,
        client_confirmed_at=now,
        confirmed=True,
        symptoms=[
            {"raw_text": "Synthetic demonstration only", "category": "high_fever"}
        ],
        food_log=[],
        supplement_check=[],
        closing_mentions=[],
    )
    result = offline_checkin.sync(
        UUID(users["patient"]["id"]), request, str(request.client_submission_id)
    )
    assert (
        offline_checkin.sync(
            UUID(users["patient"]["id"]), request, str(request.client_submission_id)
        )
        == result
    )
    data.current_user_id.set(users["clinician"]["id"])
    portal.acknowledge(
        UUID(users["patient"]["id"]), UUID(result["alert_id"]), "demo-acknowledgement"
    )
    data.current_user_id.set(users["trusted"]["id"])
    rows, _ = portal.history(UUID(users["patient"]["id"]), "alerts", 50, None)
    assert rows[0]["status"] == "acknowledged"
    data.current_user_id.set(users["patient"]["id"])
    care_access.revoke(UUID(invitations["trusted"]["id"]))
    data.current_user_id.set(users["trusted"]["id"])
    try:
        portal.read(UUID(users["patient"]["id"]), "alerts")
    except NotFound:
        pass
    else:
        raise AssertionError("Revoked recipient retained access")
    data.current_user_id.set(None)
    data.close_pool()
    report = {
        "synthetic_only": True,
        "backend_demo_passed": True,
        "duplicate_retry_verified": True,
        "acknowledgement_verified": True,
        "revocation_verified": True,
        "frontend_verified": False,
    }
    destination = Path("artifacts/operations/care-offline-demo.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print("Synthetic care/offline backend demo passed; frontend remains separate")


if __name__ == "__main__":
    main()
