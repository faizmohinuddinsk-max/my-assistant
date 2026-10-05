import json
import os

DATA_FILE = "me.json"
EXAMPLE_FILE = "me.example.json"

DEFAULT_DATA = {
    "preferences": {},
    "contacts": {},
    "alarms": [],
    "reminders": [],
    "jokes": [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I told my computer I needed a break, and it froze."
    ],
    "facts": [
        "Honey never spoils.",
        "Octopuses have three hearts."
    ],
    "saved_news": []
}


def load():
    if not os.path.exists(DATA_FILE):
        if os.path.exists(EXAMPLE_FILE):
            with open(EXAMPLE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = DEFAULT_DATA.copy()
        save(data)
        return data

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def next_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1
