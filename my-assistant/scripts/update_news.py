import os
import json
import datetime

from tavily import TavilyClient
from groq import Groq

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
NEWS_DOMAINS = ["thehindu.com", "indianexpress.com"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)
groq = Groq(api_key=GROQ_API_KEY)


def search(query):
    # Tavily's recency filter is in whole days, not hours — "1" is the
    # closest available to a 12-hour window on the free tier.
    result = tavily.search(
        query=query,
        include_domains=NEWS_DOMAINS,
        days=1,
        max_results=8,
    )
    return result.get("results", [])


def summarize(kolkata_items, top_items):
    if not kolkata_items and not top_items:
        return "No recent news was found from The Hindu or Indian Express."

    def format_block(items):
        return "\n".join(f"- {i['title']}: {i.get('content', '')[:200]}" for i in items)

    prompt = (
        "You are reading a short morning news briefing out loud. Using ONLY "
        "the headlines below (from The Hindu and Indian Express), write a "
        "briefing with two short parts:\n"
        "1. Kolkata news first, 2-4 plain spoken sentences.\n"
        "2. Then top general news, 2-4 plain spoken sentences.\n"
        "No bullet points, no markdown, just natural spoken sentences. "
        "If one section has nothing, say so briefly.\n\n"
        f"KOLKATA HEADLINES:\n{format_block(kolkata_items) or '(none)'}\n\n"
        f"TOP HEADLINES:\n{format_block(top_items) or '(none)'}"
    )
    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


def main():
    kolkata_items = search("Kolkata news today")
    top_items = search("India top news today")

    summary = summarize(kolkata_items, top_items)

    all_articles = [
        {"title": a["title"], "source": a.get("url", ""), "link": a.get("url", "")}
        for a in (kolkata_items + top_items)
    ]

    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": summary,
            "articles": all_articles,
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
