import json
import subprocess
import datetime


def today_date():
    return datetime.date.today().strftime("%A, %B %d, %Y")


def todays_events():
    """
    Reads the phone's already-synced calendar via Termux:API.
    Returns a plain sentence describing today's events.
    """
    try:
        output = subprocess.run(
            ["termux-calendar-list"], capture_output=True, text=True, timeout=10
        ).stdout
        events = json.loads(output)
    except Exception:
        return f"Today is {today_date()}. I can't reach the calendar right now."

    today = datetime.date.today().isoformat()
    todays = [e for e in events if str(e.get("begin", "")).startswith(today)]

    if not todays:
        return f"Today is {today_date()}. Nothing on your calendar today."

    titles = [e.get("title", "Untitled event") for e in todays]
    return f"Today is {today_date()}. On your calendar: " + "; ".join(titles) + "."
