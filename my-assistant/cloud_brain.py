import os
import requests

import code_solver
import fun_facts

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
WOLFRAM_APP_ID = os.environ.get("WOLFRAM_APP_ID", "")
_groq_client = None


def _get_groq():
    global _groq_client
    if _groq_client is None:
        from groq import Groq
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client


def ask(prompt):
    """Generic one-off question to Groq. Returns None if unavailable."""
    if not GROQ_API_KEY:
        return None
    try:
        client = _get_groq()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def solve_math(question, data):
    """
    Three layers, in order:
    1. Local sympy — instant, offline, handles clean equations.
    2. Wolfram Alpha — a real computation engine, not a guess. Used
       for anything sympy can't parse (word problems, etc).
    3. If neither is available/works, say so plainly.
    """
    local = code_solver.solve_equation(question)
    if not local.startswith("Couldn't solve that") and not local.startswith(
        "I couldn't find a variable"
    ):
        return local

    if WOLFRAM_APP_ID:
        try:
            resp = requests.get(
                "https://api.wolframalpha.com/v1/result",
                params={"appid": WOLFRAM_APP_ID, "i": question},
                timeout=10,
            )
            if resp.status_code == 200 and resp.text.strip():
                return f"Answer: {resp.text.strip()}"
        except requests.exceptions.RequestException:
            pass

    return local  # whatever the local solver's error message was


def get_joke(data):
    if not GROQ_API_KEY:
        return fun_facts.tell_joke(data)
    try:
        client = _get_groq()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content":
                "Tell me one short, clean, original joke. Just the joke, nothing else."}],
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return fun_facts.tell_joke(data)


def search_web(query, include_domains=None, days=None):
    """
    General-purpose web search via Tavily. Returns Tavily's own short
    synthesized answer when available, else the top result's snippet.
    Returns None if Tavily isn't set up or the call fails.
    """
    if not TAVILY_API_KEY:
        return None, []
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_API_KEY)
        kwargs = {"query": query, "include_answer": True, "max_results": 5}
        if include_domains:
            kwargs["include_domains"] = include_domains
        if days:
            kwargs["days"] = days
        result = client.search(**kwargs)
        if result.get("answer"):
            return result["answer"], result.get("results", [])
        return None, result.get("results", [])
    except Exception:
        return None, []
