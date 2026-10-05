# Arthur — a personal offline-first AI assistant

Arthur is a modular personal assistant. Each capability is its own
file; `brain.py` recognizes what you said and routes it to the right
one. Nothing requires a credit card anywhere.

## 1. One-time setup

```
pip install -r requirements.txt
python -c "import nltk; nltk.download('wordnet')"
```

Tesseract (for the camera-solve feature) must also be installed
separately — it's the actual OCR engine, not just the Python wrapper.
Windows: install from the UB-Mannheim Tesseract build and make sure
it's on PATH.

## 2. API keys (all free, no card required)

Set these as environment variables (PowerShell: `setx NAME "value"`,
then restart your terminal) — never paste them directly into code.

| Variable | Used for | Get it from |
|---|---|---|
| `GROQ_API_KEY` | jokes, search answers, headline matching | console.groq.com |
| `TAVILY_API_KEY` | live web search (news, general search) | tavily.com |
| `WOLFRAM_APP_ID` | authoritative math (optional — local sympy covers most) | developer.wolframalpha.com |

Arthur works without any of these set — each feature falls back to a
local, offline version automatically. Setting the keys just upgrades
those specific features.

## 3. Run it

```
python main.py
```

## 4. Commands

```
my favorite food is pizza          weather in Kolkata
what is my favorite food           set a timer for 30 seconds
add contact mumma +911234567890    calculate 15% of 2400
call mumma                         convert 10 km to miles
remind me to water plants at 18:00 tell me a joke
show reminders                     open camera
set an alarm for 07:30             run code: print(3*7)
show alarms                        solve 2x + 3 = 7
meaning of pizza                   solve this  (photograph a problem)
spell pizza                        what's today
news / repeat the news             search for <anything>
introduce yourself                 i am awake  (routine: reminders + news)
```

## 5. The news system (separate setup, optional)

News runs on a free GitHub Actions schedule, not on your phone — this
keeps it working even when Arthur isn't open.

1. Push this repo to GitHub.
2. In the repo's Settings → Secrets and variables → Actions, add
   `GROQ_API_KEY` and `TAVILY_API_KEY` as repository secrets.
3. The workflow in `.github/workflows/update_news.yml` runs hourly,
   writing the latest briefing to `data/news.json` in the repo.
4. Edit `news.py`'s `NEWS_URL` to point at your actual GitHub
   username/repo (it has a placeholder right now).
5. You can trigger it manually anytime from the repo's Actions tab
   ("Run workflow") instead of waiting for the hourly schedule.

News is cached, not regenerated — asking Arthur for news ten times in
an hour is ten free reads of the same file, not ten searches.

## 6. The control panel (optional)

```
python app.py
```
A visual view/edit interface for alarms, reminders, contacts, and
preferences — reads and writes the same `me.json` file Arthur uses.

## 7. Project structure

```
main.py             the loop
brain.py             understands commands, routes to the right file
memory.py            loads/saves me.json
calls.py             dialing (laptop stub, real on phone)
reminders.py         reminder logic
alarms.py            alarm logic
dictionary.py        word meanings (offline, via NLTK) + spelling
weather.py            live weather (Open-Meteo, free, no key)
timer.py              countdown timers
calculator.py         arithmetic and percentages
converter.py           unit and currency conversion
fun_facts.py           jokes and facts, stored in me.json (local fallback)
launcher.py            opens apps (laptop stub, real on phone)
camera.py              takes a photo (laptop stub, real on phone)
photo_solver.py         OCR's a photo, hands it to code_solver
code_solver.py          runs Python code + local equation solving
cloud_brain.py          Groq (jokes/search/matching), Wolfram (math), Tavily (search)
news.py                 reads the cached news briefing from GitHub
calendar_module.py       reads the phone's calendar (laptop stub, real on phone)
interaction.py           self-introduction + routines (e.g. "i am awake")
app.py                   the control panel UI
theme.py                 shared colors for app.py
scripts/update_news.py    runs in GitHub Actions, not on the phone
.github/workflows/        the hourly news schedule
data/news.json            the cached news (committed by the Action)
me.json                   your private data (gitignored, not in repo)
me.example.json            sample data, safe to commit
```

## 8. Roadmap

- Move the remaining stubs (`calls.py`, `calendar_module.py`,
  `launcher.py`, `camera.py`) to real Termux calls on the phone
- Voice in/out via Termux:API
- Floating on-screen bubble (Flutter overlay, packaged as an APK)
- SMS, notes, device toggles, music control, location reminders,
  routines beyond "i am awake"
- A fine-tuned small open-source model (Colab), as a further upgrade
  to the understanding layer `brain.py`/`cloud_brain.py` provide
