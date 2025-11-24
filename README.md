# Weather Fetch

A simple Python package to fetch weather data using the free Open-Meteo API (no API key required).

## Installation
```bash
pip install free_weather
```

## Usage
```python
from weather_fetch import WeatherFetch

wf = WeatherFetch()  # no API key needed for Open-Meteo
weather = wf.get_weather("Dhaka")  # defaults to metric units

print(weather["temperature"])
print(weather["description"])
```

### Units
- `metric` for Celsius (default)
- `imperial` for Fahrenheit
- `standard` treated the same as metric

## Testing
```bash
python -m pip install -e .
python -m pip install pytest
pytest
```

The tests mock the HTTP calls; no real API calls are made, so they run offline.

## Notes
- Uses a 10-second timeout and raises `ValueError` on request or parsing errors.
- Relies on Open-Meteo geocoding to resolve city names to coordinates; ensure the city can be found.
