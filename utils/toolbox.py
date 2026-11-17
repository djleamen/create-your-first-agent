"""
utils/toolbox.py: ready-made tools your agent can use.

These are ordinary Python functions. Nothing about them is "AI". The agent
becomes powerful when the model is allowed to decide WHEN to call them.

Peek inside if you're curious, but you don't need to edit this file.
"""

import ast
import json
import operator
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Calculator: language models are surprisingly bad at arithmetic, so we give
# them a real calculator. We parse the maths ourselves instead of using eval(),
# which would let anyone run any Python code on your laptop.
# ---------------------------------------------------------------------------

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return _OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("only numbers and + - * / // % ** ( ) are allowed")


def calculate(expression):
    """Work out a maths expression like '(12 * 4) / 3'."""
    tree = ast.parse(expression.replace("^", "**"), mode="eval")
    result = _evaluate(tree.body)
    if isinstance(result, float):
        # Computers store decimals in binary, so 12.4 - 9.1 comes out as
        # 3.3000000000000007. Rounding hides that tiny error.
        result = round(result, 10)
        if result.is_integer():
            result = int(result)
    return result


# ---------------------------------------------------------------------------
# Weather: uses Open-Meteo, a free weather service that needs no API key.
# ---------------------------------------------------------------------------

_WEATHER_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "fog", 51: "light drizzle", 53: "drizzle", 55: "heavy drizzle",
    61: "light rain", 63: "rain", 65: "heavy rain", 66: "freezing rain", 67: "freezing rain",
    71: "light snow", 73: "snow", 75: "heavy snow", 77: "snow grains",
    80: "rain showers", 81: "rain showers", 82: "violent rain showers",
    85: "snow showers", 86: "heavy snow showers", 95: "thunderstorm",
    96: "thunderstorm with hail", 99: "thunderstorm with hail",
}


def _fetch_json(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.load(response)


def get_weather(city):
    """Get the current weather for a city, e.g. 'Toronto'."""
    query = urllib.parse.urlencode({"name": city, "count": 1})
    places = _fetch_json(f"https://geocoding-api.open-meteo.com/v1/search?{query}")
    if not places.get("results"):
        return f"I couldn't find a place called {city!r}."
    place = places["results"][0]

    query = urllib.parse.urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
    })
    now = _fetch_json(f"https://api.open-meteo.com/v1/forecast?{query}")["current"]
    sky = _WEATHER_CODES.get(now["weather_code"], "unknown conditions")
    return (
        f"{place['name']}, {place.get('country', '')}: {now['temperature_2m']}°C "
        f"(feels like {now['apparent_temperature']}°C), {sky}, "
        f"wind {now['wind_speed_10m']} km/h"
    )
