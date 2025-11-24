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
    wf = WeatherFetch("test-api-key")

    expected_payload = {
        "name": "Dhaka",
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 28.5, "humidity": 70},
        "wind": {"speed": 3.5},
    }

    def fake_get(url, params=None, timeout=None):
        assert url == WeatherFetch.BASE_URL
        assert params["q"] == "Dhaka"
        assert params["appid"] == "test-api-key"
        assert timeout == wf.DEFAULT_TIMEOUT
        return DummyResponse(json_data=expected_payload)

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    result = wf.get_weather("Dhaka")
    assert result == {
        "city": "Dhaka",
        "temperature": 28.5,
        "description": "clear sky",
        "humidity": 70,
        "wind_speed": 3.5,
    }


def test_get_weather_http_error(monkeypatch):
    wf = WeatherFetch("test-api-key")

    def fake_get(url, params=None, timeout=None):
        return DummyResponse(raise_for_status_exc=requests.HTTPError("Boom"))

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    with pytest.raises(ValueError):
        wf.get_weather("Dhaka")


def test_get_weather_json_error(monkeypatch):
    wf = WeatherFetch("test-api-key")

    def fake_get(url, params=None, timeout=None):
        return DummyResponse(json_error=True)

    monkeypatch.setattr("weather_fetch.main.requests.get", fake_get)

    with pytest.raises(ValueError):
        wf.get_weather("Dhaka")
