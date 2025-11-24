# fast_free_weather

Fetch current weather using the free Open-Meteo API (no API key required).

## Installation
```bash
pip install fast_free_weather
```

## Quickstart
```python
from weather_fetch import WeatherFetch  # import path stays weather_fetch

wf = WeatherFetch()  # no API key needed
weather = wf.get_weather("Dhaka")  # defaults to metric units

print(weather["city"])
print(weather["temperature"])
print(weather["description"])
```

### Units
- `metric` (default): Celsius temps, km/h wind
- `imperial`: Fahrenheit temps, mph wind
- `standard`: treated as metric

### Error handling
- Raises `ValueError` on HTTP errors, JSON parsing issues, or unknown cities.
- Uses a 10-second timeout by default; adjust via `wf.DEFAULT_TIMEOUT` if needed.

## Testing
```bash
python -m pip install -e .
python -m pip install pytest
pytest
```
Tests mock HTTP calls, so they run offline.
