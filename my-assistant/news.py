import requests

# Replace with your actual GitHub username/repo once the repo exists.
NEWS_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/my-assistant-news/main/data/news.json"
TIMEOUT = 8


def get_news():
   
    try:
        resp = requests.get(NEWS_URL, timeout=TIMEOUT)
        resp.raise_for_status()
        body = resp.json()
        return body.get("summary", "No news summary available yet."), body.get("articles", [])
    except requests.exceptions.RequestException:
        return "I couldn't reach the news service right now.", []
