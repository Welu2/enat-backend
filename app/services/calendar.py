from datetime import date, datetime, time, timedelta
from urllib.parse import urlencode


def generate_google_calendar_url(appointment_date: date, title: str = "የእናቶች ጤና ቀጠሮ (ANC Appointment)", details: str = "የእናቶች ጤና ክትትል ቀጠሮ — EnatAI Intake Summary") -> str:
    start_dt = datetime.combine(appointment_date, time(hour=9))
    end_dt = start_dt + timedelta(hours=1)
    
    fmt = "%Y%m%dT%H%M%SZ"
    dates_str = f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}"
    
    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": dates_str,
        "details": details,
    }
    return f"https://calendar.google.com/calendar/render?{urlencode(params)}"


def generate_ical_content(appointment_date: date, title: str = "የእናቶች ጤና ቀጠሮ (ANC Appointment)", details: str = "የእናቶች ጤና ክትትል ቀጠሮ — EnatAI Intake Summary") -> str:
    start_dt = datetime.combine(appointment_date, time(hour=9))
    end_dt = start_dt + timedelta(hours=1)
    fmt = "%Y%m%dT%H%M%SZ"

    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//EnatAI Maternal Health Intake//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
SUMMARY:{title}
DESCRIPTION:{details}
DTSTART:{start_dt.strftime(fmt)}
DTEND:{end_dt.strftime(fmt)}
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-P1D
ACTION:DISPLAY
DESCRIPTION:Reminder: ANC Appointment Tomorrow
END:VALARM
BEGIN:VALARM
TRIGGER:-PT2H
ACTION:DISPLAY
DESCRIPTION:Reminder: ANC Appointment in 2 Hours
END:VALARM
END:VEVENT
END:VCALENDAR"""
