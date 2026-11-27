
from fastmcp import FastMCP
import requests

mcp = FastMCP("Weather Server")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_description(code):
    """Convert WMO weather codes into readable descriptions."""

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    return weather_codes.get(code, "Unknown weather condition")


@mcp.tool()
def get_weather(city: str):
    """
    Fetch actual current weather conditions for any supported city.

    Args:
        city: City name, e.g. Delhi, London, Pune.

    Returns:
        Current weather information.
    """

    try:
        # Step 1: Find city coordinates
        geo_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"City not found: {city}"

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location["name"]
        country = location.get("country", "Unknown")

        # Step 2: Fetch current weather
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        # Step 3: Extract weather details
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        feels_like = current["apparent_temperature"]
        wind_speed = current["wind_speed_10m"]

        condition = get_weather_description(
            current["weather_code"]
        )

        observation_time = current["time"]

        # Step 4: Return readable result
        return (
            f"Weather in {city_name}, {country}\n"
            f"Condition: {condition}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} km/h\n"
            f"Observation Time: {observation_time}"
        )

    except requests.RequestException as e:
        return f"Weather API error: {str(e)}"

    except (KeyError, ValueError) as e:
        return f"Unable to process weather data: {str(e)}"



@mcp.tool()
def get_weather_forecast(city: str, days: int = 7):
    """
    Fetch daily weather forecast for a city.

    Args:
        city: City name, e.g. Pune, Delhi, London.
        days: Number of forecast days (1 to 16).

    Returns:
        Daily weather forecast.
    """

    try:
        # Validate forecast days
        if not 1 <= days <= 16:
            return "Forecast days must be between 1 and 16."

        # Step 1: Get city coordinates
        geo_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"City not found: {city}"

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location["name"]
        country = location.get("country", "Unknown")

        # Step 2: Fetch daily forecast
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_probability_max,"
                    "precipitation_sum,"
                    "wind_speed_10m_max"
                ),
                "timezone": "auto",
                "forecast_days": days
            },
            timeout=10
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        daily = weather_data["daily"]

        # Step 3: Format forecast
        forecast = []

        for i, date in enumerate(daily["time"]):

            condition = get_weather_description(
                daily["weather_code"][i]
            )

            max_temp = daily["temperature_2m_max"][i]
            min_temp = daily["temperature_2m_min"][i]

            rain_probability = daily[
                "precipitation_probability_max"
            ][i]

            precipitation = daily["precipitation_sum"][i]
            wind_speed = daily["wind_speed_10m_max"][i]

            forecast.append(
                f"Date: {date}\n"
                f"Condition: {condition}\n"
                f"Temperature: {min_temp}°C - {max_temp}°C\n"
                f"Rain Probability: {rain_probability}%\n"
                f"Precipitation: {precipitation} mm\n"
                f"Maximum Wind Speed: {wind_speed} km/h"
            )

        # Step 4: Return complete forecast
        return (
            f"Weather Forecast for {city_name}, {country}\n"
            f"Forecast Days: {days}\n\n"
            + "\n\n".join(forecast)
        )

    except requests.RequestException as e:
        return f"Weather API error: {str(e)}"

    except (KeyError, ValueError, TypeError) as e:
        return f"Unable to process forecast data: {str(e)}"



if __name__ == "__main__":
    print("Starting Weather MCP Server...")
    mcp.run()
