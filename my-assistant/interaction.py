import reminders
import news


def introduce_self():
    return "I'm Arthur, an Artificial Assistant created by a asshole called Faiz."


def i_am_awake(data):
  
    reminder = reminders.list_open(data)
    news = news.get_news()
    return f"Good morning. {reminder} For the news: {news}"
