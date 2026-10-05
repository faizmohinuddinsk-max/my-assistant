"""brain.py: Arthur's command matching system, understanding, and gides the ystem to what to do. it regulates choices by commands and oreferences"""

import memory
import reminders
import alarms
import dictionary
import weather
import timer
import calculator
import converter
import fun_facts
import launcher
import code_solver
import camera
import photo_solver
import cloud_brain
import news
import calendar_module
import interaction
import local_llm


def save_news_item(answer, articles, data):
    """Saves news and article stuff"""
    if not articles:
        return "There's nothing to save right now."

    titles = [a["title"] for a in articles]
    matched_title = None

    listing = "\n".join(f"{i}. {t}" for i, t in enumerate(titles))
    reply = cloud_brain.ask(
        "Here is a numbered list of news headlines:\n" + listing +
        f'\n\nThe user said: "{answer}"\n'
        "Which headline number do they mean? Reply with ONLY the number. "
        "If none match, reply with -1."
    )
    if reply is not None:
        try:
            index = int(reply.strip())
            if 0 <= index < len(titles):
                matched_title = titles[index]
        except ValueError:
            pass

    if matched_title is None:
        answer_words = set(answer.lower().split())
        best, best_score = None, 0
        for a in articles:
            score = len(answer_words & set(a["title"].lower().split()))
            if score > best_score:
                best, best_score = a, score
        if best:
            matched_title = best["title"]

    if matched_title is None:
        return "I couldn't tell which one you meant — nothing saved."

    chosen = next(a for a in articles if a["title"] == matched_title)
    data["saved_news"].append(chosen)
    return f'Saved: "{matched_title}"'


def handle(text, data, pending):
 
    text = text.strip()          
    lower = text.lower()       
    # STEP 1 — Were we in the middle of asking "yes or no"?
    if pending:
        if pending.get("type") == "news_save_offer":
            if lower in ("yes", "yeah", "yep", "hae", "হ্যাঁ"):
                return "Which one should I save?", {
                    "type": "news_save_which",
                    "articles": pending["articles"]
                }
            if lower in ("no", "nope", "না"):
                return "Okay, nothing saved.", None
            return "Should I save anything from that? Yes or no.", pending

        if pending.get("type") == "news_save_which":
            return save_news_item(text, pending["articles"], data), None

        if lower in ("yes", "yeah", "yep", "confirm", "hae", "হ্যাঁ"):
            return pending["confirm_reply"], None

        if lower in ("no", "nope", "cancel", "না"):
            return "Okay, cancelled.", None

        return "Please say yes or no.", pending
    
    # STEP 2 — Preferences: "my favorite X is Y"
  
    if lower.startswith("my favorite ") and " is " in lower:
        rest = text[len("my favorite "):]
        key, _, value = rest.partition(" is ")
        data["preferences"][key.strip().lower()] = value.strip()
        return f"Got it — favorite {key.strip()} is {value.strip()}.", None

    if lower.startswith("what is my favorite") or lower.startswith("what's my favorite"):
        key = lower.split("favorite", 1)[1].strip().rstrip("?")
        value = data["preferences"].get(key)
        if value:
            return f"Your favorite {key} is {value}.", None
        return f"I don't know your favorite {key} yet.", None

 
    # STEP 3 — Calls

    if lower.startswith("call ") or lower.startswith("কল "):
        name = text.split(" ", 1)[1].strip().lower()

        if name in data["contacts"]:
            pending_action = {
                "type": "call",
                "name": name,
                "confirm_reply": f"Calling {name} on speaker."
            }
            return f"Call {name}, right?", pending_action
        
        return f"I don't have a contact called {name}.", None


    # STEP 4 — Reminders
  
    if lower.startswith("remind me to "):
        rest = text[len("remind me to "):]
        if " at " in rest:
            note, _, time_str = rest.rpartition(" at ")
        else:
            note, time_str = rest, "unspecified"
        return reminders.add(data, note, time_str), None

    if lower in ("show reminders", "list reminders", "what are my reminders"):
        return reminders.list_open(data), None

    
    # STEP 5 — Alarms
    
    if lower.startswith("set an alarm for ") or lower.startswith("set alarm for "):
        time_str = text.rsplit(" for ", 1)[1].strip()
        return alarms.add(data, time_str), None

    if lower in ("show alarms", "list alarms", "what are my alarms"):
        return alarms.list_enabled(data), None

   
    # STEP 6 — Adding a contact: "add contact NAME NUMBER"
    
    if lower.startswith("add contact "):
        parts = text[len("add contact "):].split()
        if len(parts) >= 2:
            name, number = parts[0].lower(), parts[1]
            data["contacts"][name] = number
            return f"Saved {name} as {number}.", None
        return "Say it like: add contact mumma +911234567890", None

   
    # STEP 7 — Dictionary
    
    if lower.startswith("meaning of "):
        return dictionary.meaning(text[len("meaning of "):].strip()), None

    if lower.startswith("spell "):
        return dictionary.spell(text[len("spell "):].strip()), None

   
    # STEP 8 — Weather
  
    if lower.startswith("weather in "):
        return weather.get_weather(text[len("weather in "):].strip()), None

    
    # STEP 9 — Timer
   
    if lower.startswith("set a timer for ") or lower.startswith("set timer for "):
        rest = text.split(" for ", 1)[1].strip()
        parts = rest.split()
        amount = float(parts[0])
        unit = parts[1] if len(parts) > 1 else "seconds"
        seconds = amount * 60 if "min" in unit else amount
        return timer.start_timer(seconds), None

   
    # STEP 10 — Calculator
   
    if lower.startswith("calculate "):
        return calculator.calculate(text[len("calculate "):]), None

   
    # STEP 11 — Converter, covert dintance and stuff
    
    if lower.startswith("convert "):
        rest = text[len("convert "):]
        parts = rest.split()
        if len(parts) >= 4 and parts[2].lower() == "to":
            value, from_unit, _, to_unit = parts[0], parts[1], parts[2], parts[3]
            try:
                value = float(value)
            except ValueError:
                return "Say it like: convert 10 km to miles", None

            if from_unit.upper() in ("USD", "EUR", "GBP", "INR", "JPY"):
                result = converter.convert_currency(value, from_unit, to_unit)
            else:
                result = converter.convert_units(value, from_unit, to_unit)

            if result is None:
                return f"I don't know how to convert {from_unit} to {to_unit}.", None
            return f"{value} {from_unit} is {result} {to_unit}.", None
        return "Say it like: convert 10 km to miles", None

    
    # STEP 12 — Fun facts: "tell me a joke" / "tell me a fact"
    
    if lower in ("tell me a joke", "joke"):
        return cloud_brain.get_joke(data), None

    if lower in ("tell me a fact", "fact"):
        return fun_facts.tell_fact(data), None


    # STEP 13 — App launcher: "open X"

    if lower.startswith("open "):
        return launcher.open_app(text[len("open "):].strip()), None


    # STEP 14 — Run Python code: "run code: ..."
  
    if lower.startswith("run code:"):
        code = text.split(":", 1)[1].strip()
        return code_solver.run_code(code), None

  
    # STEP 15 — Camera: "solve this" (photographs a problem and solves it)

    if lower in ("solve this", "take a photo", "take photo", "solve from photo"):
        path = camera.take_photo()
        if path is None:
            return "No camera available here (laptop stub).", None
        return photo_solver.solve_from_image(path), None

   
    # STEP 16 — Solve equations: "solve ..."
   
    if lower.startswith("solve "):
        return cloud_brain.solve_math(text[len("solve "):].strip(), data), None

   
    # STEP 17 — News: "what's the news" / "news"

    if lower in ("what's the news", "whats the news", "news", "tell me the news",
                 "repeat the news", "what was the news", "what was today's news"):
        summary, articles = news.get_news()
        reply = (
            summary +
            " This isn't saved anywhere — I'll forget it once we're done. "
            "Want me to save anything from it?"
        )
        pending_action = {"type": "news_save_offer", "articles": articles}
        return reply, pending_action

  
    # STEP 18 — Calendar: "what's today" / "date and events"
  
    if lower in ("what's today", "whats today", "what day is it",
                 "what's on today", "date and events", "today's events"):
        return calendar_module.todays_events(), None

 
    # STEP 19 — Identity & routines: "who are you" / "I am awake"

    if lower in ("introduce yourself", "who are you", "what are you"):
        return interaction.introduce_self(), None

    if lower in ("i am awake", "i'm awake", "good morning"):
        return interaction.i_am_awake(data), None

 
    # STEP 19b — General search: "search for X" / "look up X"

    if lower.startswith("search for ") or lower.startswith("look up "):
        query = text.split(" ", 2)[2] if lower.startswith("look up ") else text[len("search for "):]
        answer, _ = cloud_brain.search_web(query.strip())
        return answer or "I couldn't find anything on that right now.", None

 
    # STEP 20 — Fallback: nothing matched above
  
    local_reply = local_llm.ask(text)
    if local_reply:
        return local_reply, None

    return "I don't know that one yet.", None