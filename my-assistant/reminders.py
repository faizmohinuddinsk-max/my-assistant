import memory


def add(data, note, time_str):

    new_id = memory.next_id(data["reminders"])
    data["reminders"].append({
        "id": new_id,
        "time": time_str.strip(),
        "text": note.strip(),
        "done": False
    })
    return f"Reminder set: {note.strip()} at {time_str.strip()}."


def list_open(data):
    """List every reminder that hasn't been marked done yet."""
    open_ones = [r for r in data["reminders"] if not r["done"]]
    if not open_ones:
        return "No open reminders."
    lines = [f'{r["time"]} — {r["text"]}' for r in open_ones]
    return "Your reminders: " + "; ".join(lines)


def mark_done(data, reminder_id):
    """Mark one reminder as completed, by its id."""
    for r in data["reminders"]:
        if r["id"] == reminder_id:
            r["done"] = True
            return f'Marked "{r["text"]}" as done.'
    return "Couldn't find that reminder."


def delete(data, reminder_id):
    """Remove a reminder completely, by its id."""
    before = len(data["reminders"])
    data["reminders"] = [r for r in data["reminders"] if r["id"] != reminder_id]
    if len(data["reminders"]) < before:
        return "Reminder deleted."
    return "Couldn't find that reminder."
