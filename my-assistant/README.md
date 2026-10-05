# Arthur: My First offline-first AI assistant

Arthur is a modular personal assistant. Each capability is its own
file; `brain.py` recognizes what you said and routes it to the right
one. Nothing requires a credit card anywhere.

## Using API keys (all free, no card required)

| Variable | Used for | Get it from |
|---|---|---|
| `GROQ_API_KEY` | jokes, search answers, headline matching | console.groq.com |
| `TAVILY_API_KEY` | live web search (news, general search) | tavily.com |
| `WOLFRAM_APP_ID` | authoritative math (optional — local sympy covers most) | developer.wolframalpha.com |

Arthur works without any of these, each feature falls back to a
local, offline version automatically. Setting the keys just upgrades
those specific features.

## The news system, still a work in progress

News runs on a free GitHub Actions schedule, not on any device — this
keeps it working even when Arthur isn't open.

## Project structure

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
