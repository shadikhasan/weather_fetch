import pytest
import requests

from weather_fetch import WeatherFetch


class DummyResponse:
    def __init__(self, *, json_data=None, raise_for_status_exc=None, json_error=False):
        self._json_data = json_data or {}
        self._raise_for_status_exc = raise_for_status_exc
        self._json_error = json_error

    def raise_for_status(self):
        if self._raise_for_status_exc:
            raise self._raise_for_status_exc

    def json(self):
        if self._json_error:
            raise ValueError("Invalid JSON")
        return self._json_data


def test_get_weather_success(monkeypatch):
    wf = WeatherFetch()

    geocode_payload = {
        "results": [
            {"name": "Dhaka", "latitude": 23.81, "longitude": 90.41},
        ]
    }
    forecast_payload = {
        "current": {
            "temperature_2m": 28.5,
            "relativehumidity_2m": 70,
            "wind_speed_10m": 3.5,
            "weathercode": 1,
        }
    }

    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append(url)
        if url == WeatherFetch.GEOCODE_URL:
            return DummyResponse(json_data=geocode_payload)
        if url == WeatherFetch.FORECAST_URL:
            assert params["latitude"] == 23.81
            assert params["longitude"] == 90.41
            assert params["temperature_unit"] == "celsius"
            assert params["wind_speed_unit"] == "kmh"
            return DummyResponse(json_data=forecast_payload)
        raise AssertionError("Unexpected URL")

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    result = wf.get_weather("Dhaka")
    assert calls == [WeatherFetch.GEOCODE_URL, WeatherFetch.FORECAST_URL]
    assert result == {
        "city": "Dhaka",
        "temperature": 28.5,
        "description": WeatherFetch.WEATHER_CODE_DESCRIPTIONS[1],
        "humidity": 70,
        "wind_speed": 3.5,
    }


def test_get_weather_geocode_not_found(monkeypatch):
    wf = WeatherFetch()

    def fake_get(url, params=None, timeout=None):
        if url == WeatherFetch.GEOCODE_URL:
            return DummyResponse(json_data={"results": []})
        return DummyResponse()

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    with pytest.raises(ValueError):
        wf.get_weather("Unknown City")


def test_get_weather_http_error(monkeypatch):
    wf = WeatherFetch()

    def fake_get(url, params=None, timeout=None):
        if url == WeatherFetch.GEOCODE_URL:
            return DummyResponse(json_data={"results": [{"latitude": 1, "longitude": 2}]})
        return DummyResponse(raise_for_status_exc=requests.HTTPError("Boom"))

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    with pytest.raises(ValueError):
        wf.get_weather("Dhaka")


def test_get_weather_json_error(monkeypatch):
    wf = WeatherFetch()

    def fake_get(url, params=None, timeout=None):
        if url == WeatherFetch.GEOCODE_URL:
            return DummyResponse(json_data={"results": [{"latitude": 1, "longitude": 2}]})
        return DummyResponse(json_error=True)

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    with pytest.raises(ValueError):
        wf.get_weather("Dhaka")
