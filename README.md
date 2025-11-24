# Weather Fetch

A simple Python package to fetch weather data from the OpenWeatherMap API.

## Installation
```bash
pip install weather-fetch
```

## Usage
```python
from weather_fetch import WeatherFetch

wf = WeatherFetch(api_key="YOUR_OPENWEATHERMAP_API_KEY")
weather = wf.get_weather("Dhaka")  # defaults to metric units

print(weather["temperature"])
print(weather["description"])
```

### Units
- `metric` for Celsius (default)
- `imperial` for Fahrenheit
- `standard` for Kelvin

## Testing
```bash
python -m pip install -e .
python -m pip install pytest
pytest
```

The tests mock the HTTP calls; no real API calls are made, so they run offline.

## Notes
- The client uses a 10-second timeout and raises `ValueError` on request or parsing errors.
- You need a valid OpenWeatherMap API key to fetch real data.
