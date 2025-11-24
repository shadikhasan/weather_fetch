import requests

class WeatherFetch:
    """
    A simple class to fetch weather data from OpenWeatherMap API.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        """
        Initialize with your OpenWeatherMap API key.
        """
        self.api_key = api_key

    def get_weather(self, city: str, units: str = "metric") -> dict:
        """
        Fetch current weather for a given city.
        Args:
            city (str): City name
            units (str): 'metric' for Celsius, 'imperial' for Fahrenheit, 'standard' for Kelvin
        Returns:
            dict: Weather data containing temperature, description, humidity, etc.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            raise ValueError(f"Error fetching weather data: {response.text}")

        data = response.json()
        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
