from datetime import date, datetime, time

from app.core.clock import LOCAL_ZONE, utc_now
from app.db.repositories.appointments import AppointmentRepository
from app.db.repositories.reminders import ReminderRepository
from app.db.repositories.supplements import SupplementRepository
from app.db.repositories.users import UserRepository
from app.services.summary import SummaryService


class ReminderService:
    def __init__(self, clock=utc_now):
        self.clock = clock
        self.users = UserRepository()
        self.appointments = AppointmentRepository(clock)
        self.supplements = SupplementRepository(clock)
        self.reminders = ReminderRepository(clock)
        self.summary_service = SummaryService(clock)

    def list_pending(self, user_id):
        return self.reminders.list_pending(user_id)

    def run_user_day(self, user_id, occurrence):
        today = self.clock().astimezone(LOCAL_ZONE).date()
        # Recover all queue/checkpoint progress, but never issue stale dose prompts
        # or fabricate historical snapshots from today's profile and appointments.
        if occurrence != today or not self.users.get_by_id(user_id):
            return
        self.summary_service.check_and_generate_auto_summary(user_id)
        appointment = self.appointments.get_by_user(user_id)

        def create(kind, related, hour, message):
            due = datetime.combine(today, hour, LOCAL_ZONE)
            self.reminders.create_once(
                user_id, kind, message, due, f"{kind}:{related}:{due.isoformat()}"
            )

        if not appointment or appointment.get("status", "scheduled") != "scheduled":
            create(
                "set_appointment",
                "none",
                time(9),
                "Please set your next ANC appointment.",
            )
        else:
            apt_date = date.fromisoformat(str(appointment["appointment_date"])[:10])
            if 0 <= (apt_date - today).days <= appointment.get("reminder_lead_days", 2):
                create(
                    "appointment_approaching",
                    f"{appointment['id']}:{apt_date}",
                    time(8),
                    "Your ANC appointment is approaching.",
                )
        for supplement in self.supplements.list_active(user_id):
            if supplement.get("reminder_enabled"):
                reminder_time = time.fromisoformat(
                    str(supplement.get("reminder_time") or "09:00:00")
                )
                create(
                    "supplement",
                    supplement["id"],
                    reminder_time,
                    f"Reminder to take your {supplement['name']} supplement.",
                )
