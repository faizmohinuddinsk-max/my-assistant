import re


def calculate(text):
    percent_match = re.match(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)", text)
    if percent_match:
        pct, base = float(percent_match.group(1)), float(percent_match.group(2))
        return str(round(pct / 100 * base, 2))

    cleaned = re.sub(r"[^0-9+\-*/().\s]", "", text)
    try:
        return str(eval(cleaned))
    except Exception:
        return "I couldn't calculate that."
