import pytest
from app.services.pollutant_analysis_service import analyze_pollutants

def test_analyze_pollutants_safe():
    data = {
        "pm25": 10,
        "pm10": 20,
        "no2": 15,
        "so2": 10,
        "co": 1,
        "ozone": 20
    }
    result = analyze_pollutants(data)
    assert result["major_pollutant"] is not None
    assert "No pollutants are currently exceeding safe limits." in result["explanation"]

def test_analyze_pollutants_unsafe():
    data = {
        "pm25": 100, # Exceeds 60
        "pm10": 20,
        "no2": 15,
        "so2": 10,
        "co": 1,
        "ozone": 20
    }
    result = analyze_pollutants(data)
    assert result["major_pollutant"]["name"].upper() == "PM25"
    assert "exceeds the safe limit" in result["explanation"]
