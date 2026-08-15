from datetime import date, datetime, time, timedelta
from typing import Any
from uuid import UUID

from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.reminders import ReminderRepository
from app.db.repositories.supplements import SupplementRepository
from app.db.repositories.users import UserRepository
from app.services.summary import SummaryService


class ReminderService:
    def __init__(self) -> None:
        self.users = UserRepository()
        self.appointments = AppointmentRepository()
        self.supplements = SupplementRepository()
        self.reminders = ReminderRepository()
        self.summary_service = SummaryService()

    def list_pending(self, user_id: UUID) -> list[dict[str, Any]]:
        return self.reminders.list_pending(user_id)

    def run_daily_job(self) -> dict[str, int]:
        created = {"set_appointment": 0, "supplement": 0, "appointment_approaching": 0, "auto_summary": 0}
        today = date.today()

        for user in self.users.list_all():
            user_id = UUID(user["id"])

            # Automatic clinician summary check (1 day before appointment or 30-day monthly fallback)
            auto_summary = self.summary_service.check_and_generate_auto_summary(user_id)
            if auto_summary:
                created["auto_summary"] += 1

            appointment = self.appointments.get_by_user(user_id)

            if not appointment:
                due_at = datetime.combine(today, time(hour=9))
                if not self.reminders.exists_for_today(user_id, "set_appointment", due_at):
                    self.reminders.create(
                        user_id,
                        {
                            "type": "set_appointment",
                            "message": "Please set your next ANC appointment.",
                            "due_at": due_at.isoformat(),
                        },
                    )
                    created["set_appointment"] += 1
            else:
                appointment_date = date.fromisoformat(appointment["appointment_date"])
                lead_days = appointment.get("reminder_lead_days", 2)
                days_until = (appointment_date - today).days

                if 0 <= days_until <= lead_days:
                    due_at = datetime.combine(today, time(hour=8))
                    if not self.reminders.exists_for_today(
                        user_id, "appointment_approaching", due_at
                    ):
                        self.reminders.create(
                            user_id,
                            {
                                "type": "appointment_approaching",
                                "message": "Your ANC appointment is approaching.",
                                "due_at": due_at.isoformat(),
                            },
                        )
                        created["appointment_approaching"] += 1

            for supplement in self.supplements.list_active(user_id):
                if not supplement.get("reminder_enabled"):
                    continue
                reminder_time = supplement.get("reminder_time") or "09:00:00"
                if isinstance(reminder_time, str):
                    hour, minute, *_ = reminder_time.split(":")
                    due_at = datetime.combine(today, time(hour=int(hour), minute=int(minute)))
                else:
                    due_at = datetime.combine(today, time(hour=9))

                if not self.reminders.exists_for_today(user_id, "supplement", due_at):
                    self.reminders.create(
                        user_id,
                        {
                            "type": "supplement",
                            "message": f"Reminder to take your {supplement['name']} supplement.",
                            "due_at": due_at.isoformat(),
                        },
                    )
                    created["supplement"] += 1

        return created
