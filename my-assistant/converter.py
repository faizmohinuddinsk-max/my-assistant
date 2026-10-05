import requests

UNIT_TABLE = {
    ("km", "miles"): 0.621371,
    ("miles", "km"): 1.60934,
    ("kg", "lbs"): 2.20462,
    ("lbs", "kg"): 0.453592,
    ("celsius", "fahrenheit"): None,
    ("fahrenheit", "celsius"): None,
    ("liters", "gallons"): 0.264172,
    ("gallons", "liters"): 3.78541,
}


def convert_units(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.lower(), to_unit.lower()

    if from_unit == "celsius" and to_unit == "fahrenheit":
        return round(value * 9 / 5 + 32, 2)
    if from_unit == "fahrenheit" and to_unit == "celsius":
        return round((value - 32) * 5 / 9, 2)

    factor = UNIT_TABLE.get((from_unit, to_unit))
    if factor is None:
        return None
    return round(value * factor, 2)


def convert_currency(amount, from_code, to_code):
    resp = requests.get(f"https://open.er-api.com/v6/latest/{from_code.upper()}").json()
    rate = resp.get("rates", {}).get(to_code.upper())
    if rate is None:
        return None
    return round(amount * rate, 2)
