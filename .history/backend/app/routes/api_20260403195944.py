from fastapi import APIRouter
from services.data_service import get_nearest_station, get_station_data

router = APIRouter()

CAUSES = {
    "PM2.5": "Vehicle exhaust, industrial emissions, and dust.",
    "PM10": "Construction dust, road dust, and windblown soil."
}

def get_health_advice(aqi):
    if aqi <= 50: return "Good", "Enjoy outdoor activities."
    elif aqi <= 100: return "Moderate", "Sensitive groups should limit prolonged exertion."
    elif aqi <= 200: return "Poor", "Wear an N95 mask outdoors. Run air purifiers."
    return "Severe", "Avoid all outdoor physical activity. Keep windows closed."

@router.get("/api/aqi")
def fetch_dashboard_data(lat: float, lon: float):
    station_name = get_nearest_station(lat, lon)
    latest_data, predictions = get_station_data(station_name)
    
    aqi = latest_data.get('AQI', 0)
    primary_pollutant = latest_data.get('Highest Pollutant', 'PM2.5')
    risk_level, advice = get_health_advice(aqi)
    
    return {
        "station": station_name,
        "current": {
            "aqi": aqi,
            "pm25": latest_data.get('PM2.5 (ug/m3)', 'N/A'),
            "pm10": latest_data.get('PM10 (ug/m3)', 'N/A'),
            "primary": primary_pollutant
        },
        "insights": {
            "causes": CAUSES.get(primary_pollutant, "General urban pollution mix."),
            "risk_level": risk_level,
            "prevention": advice
        },
        "predictions": predictions # List of 12 predicted AQI numbers
    }