import requests
from typing import Any, Dict, Optional


class WeatherFetch:
    """
    A simple class to fetch weather data from OpenWeatherMap API.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    DEFAULT_TIMEOUT = 10  # seconds

    def __init__(self, api_key: str):
        """
        Initialize with your OpenWeatherMap API key.
        """
        self.api_key = api_key

    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Optional[Any]]:
        """
        Fetch current weather for a given city.
        Args:
            city (str): City name
            units (str): 'metric' for Celsius, 'imperial' for Fahrenheit, 'standard' for Kelvin
        Returns:
            dict: Weather data containing temperature, description, humidity, etc.
        Raises:
            ValueError: If the API request fails or returns an unexpected response.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ValueError(f"Error fetching weather data: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:  # JSON decoding error
            raise ValueError("Error parsing weather data response as JSON") from exc

        weather_list = data.get("weather") or []
        weather_info = weather_list[0] if weather_list else {}
        main_info = data.get("main", {})
        wind_info = data.get("wind", {})

        return {
            "city": data.get("name"),
            "temperature": main_info.get("temp"),
            "description": weather_info.get("description"),
            "humidity": main_info.get("humidity"),
            "wind_speed": wind_info.get("speed"),
        }
