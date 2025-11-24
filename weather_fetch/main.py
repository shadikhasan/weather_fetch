import requests
from typing import Any, Dict, Optional, Tuple


class WeatherFetch:
    """
    A simple class to fetch weather data using the Open-Meteo API (no API key required).
    """

    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    DEFAULT_TIMEOUT = 10  # seconds

    WEATHER_CODE_DESCRIPTIONS: Dict[int, str] = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        56: "freezing light drizzle",
        57: "freezing dense drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        66: "light freezing rain",
        67: "heavy freezing rain",
        71: "slight snow fall",
        73: "moderate snow fall",
        75: "heavy snow fall",
        77: "snow grains",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        85: "slight snow showers",
        86: "heavy snow showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail",
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the client. The api_key is unused for Open-Meteo but kept for API compatibility.
        """
        self.api_key = api_key

    def _geocode(self, city: str) -> Tuple[float, float, Optional[str]]:
        """Resolve a city name to latitude/longitude using Open-Meteo geocoding."""
        params = {
            "name": city,
            "count": 1,
        }
        try:
            response = requests.get(self.GEOCODE_URL, params=params, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise ValueError(f"Error fetching geocoding data: {exc}") from exc
        except ValueError as exc:
            raise ValueError("Error parsing geocoding response as JSON") from exc

        results = data.get("results") or []
        if not results:
            raise ValueError(f"Could not find coordinates for city '{city}'")

        location = results[0]
        return (
            location.get("latitude"),
            location.get("longitude"),
            location.get("name"),
        )

    def _unit_params(self, units: str) -> Dict[str, str]:
        """Translate simple unit choice to Open-Meteo parameters."""
        units = units.lower()
        if units not in {"metric", "imperial", "standard"}:
            raise ValueError("Units must be one of: metric, imperial, standard")

        if units == "imperial":
            return {"temperature_unit": "fahrenheit", "wind_speed_unit": "mph"}
        return {"temperature_unit": "celsius", "wind_speed_unit": "kmh"}

    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Optional[Any]]:
        """
        Fetch current weather for a given city.
        Args:
            city (str): City name
            units (str): 'metric', 'imperial', or 'standard'
        Returns:
            dict: Weather data containing temperature, description, humidity, etc.
        Raises:
            ValueError: If the API request fails or returns an unexpected response.
        """
        latitude, longitude, resolved_name = self._geocode(city)

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relativehumidity_2m,wind_speed_10m,weathercode",
            **self._unit_params(units),
        }

        try:
            response = requests.get(self.FORECAST_URL, params=params, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise ValueError(f"Error fetching weather data: {exc}") from exc
        except ValueError as exc:
            raise ValueError("Error parsing weather data response as JSON") from exc

        current = data.get("current") or {}
        weather_code = current.get("weathercode")

        return {
            "city": resolved_name or city,
            "temperature": current.get("temperature_2m"),
            "description": self.WEATHER_CODE_DESCRIPTIONS.get(weather_code),
            "humidity": current.get("relativehumidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
        }
