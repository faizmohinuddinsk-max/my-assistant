import requests


def get_weather(city):
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1}
    ).json()

    if not geo.get("results"):
        return f"I couldn't find a place called {city}."

    place = geo["results"][0]
    lat, lon = place["latitude"], place["longitude"]

    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True}
    ).json()

    current = forecast["current_weather"]
    temp = current["temperature"]
    wind = current["windspeed"]

    return f"It's currently {temp}°C in {place['name']}, wind {wind} km/h."
