"""Alarm system"""

import memory

def add(data, time_str, label="Alarm", sound="sounds/default.mp3"):
    """Add a new alarm at the given time, with an optional label and sound."""
    new_id = memory.next_id(data["alarms"])
    data["alarms"].append({
        "id": new_id,
        "time": time_str.strip(),
        "label": label,
        "sound": sound,
        "enabled": True
    })
    return f"Alarm set for {time_str.strip()}."


def list_enabled(data):
    """List every alarm that's currently switched on."""
    if not data["alarms"]:
        return "No alarms set."
    lines = [f'{a["time"]} — {a["label"]}' for a in data["alarms"] if a["enabled"]]
    if not lines:
        return "All your alarms are turned off."
    return "Your alarms: " + "; ".join(lines)


def toggle(data, alarm_id, enabled):
    """Turn one alarm on or off, by its id. `enabled` is True or False."""
    for a in data["alarms"]:
        if a["id"] == alarm_id:
            a["enabled"] = enabled
            state = "on" if enabled else "off"
            return f'Alarm at {a["time"]} turned {state}.'
    return "Couldn't find that alarm."


def delete(data, alarm_id):
    """Remove an alarm completely, by its id."""
    before = len(data["alarms"])
    data["alarms"] = [a for a in data["alarms"] if a["id"] != alarm_id]
    if len(data["alarms"]) < before:
        return "Alarm deleted."
    return "Couldn't find that alarm."
