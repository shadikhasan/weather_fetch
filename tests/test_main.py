from weather_fetch import WeatherFetch

def test_weather_fetch():
    api_key = "YOUR_API_KEY"  # Replace with real API key for testing
    wf = WeatherFetch(api_key)
    
    result = wf.get_weather("Dhaka")
    assert "temperature" in result
    assert "description" in result
