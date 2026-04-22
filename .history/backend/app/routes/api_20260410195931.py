from fastapi import APIRouter, HTTPException
from services.data_service import get_nearest_station, get_station_payload, get_top_polluted

router = APIRouter()

# Dictionaries to map chemical pollutants to causes
CAUSES = {
    "PM2.5": "Vehicle exhaust, industrial emissions, and fine dust.",
    "PM10": "Construction dust, road dust, and windblown soil.",
    "NO2": "Heavy traffic and fossil fuel combustion.",
    "SO2": "Industrial activities and power plants.",
    "Ozone": "Chemical reactions between pollutants and sunlight.",
    "CO": "Incomplete combustion of fuels from vehicles."
}

# ✨ NEW: Actionable steps to actively REDUCE the pollution (Systemic/Individual)
REDUCTION_TIPS = {
    "PM2.5": ["Use public transport.", "Avoid burning garbage or wood.", "Transition to electric vehicles."],
    "PM10": ["Cover open construction sites.", "Pave dirt roads.", "Plant broad-leaf dust-absorbing trees (e.g., Neem)."],
    "NO2": ["Maintain vehicle engines regularly.", "Use energy-efficient appliances.", "Carpool during peak hours."],
    "SO2": ["Use low-sulfur fuels.", "Promote solar/wind energy in local industries."],
    "Ozone": ["Fuel vehicles in the evening.", "Reduce use of VOC-heavy paints and solvents."],
    "CO": ["Regularly service gas heaters.", "Do not idle car engines in traffic."]
}

def get_health_intelligence(aqi):
    """Returns Risk Category and Personal Preventive Measure"""
    try: aqi = float(aqi)
    except: return "Unknown", "Data unavailable."

    if aqi <= 50: return "Good", "Air quality is satisfactory. Enjoy outdoor activities."
    elif aqi <= 100: return "Satisfactory", "Minor breathing discomfort to sensitive people."
    elif aqi <= 200: return "Moderate", "Asthma patients should limit heavy exertion outdoors."
    elif aqi <= 300: return "Poor", "Wear an N95 mask outdoors. Run air purifiers indoors."
    elif aqi <= 400: return "Very Poor", "Respiratory illness on prolonged exposure. Avoid outdoors."
    else: return "Severe", "Healthy people will be affected. Stop all outdoor physical activities."

# --- Existing Route (Expanded with Reduction Tips) ---
@router.get("/api/aqi")
def fetch_air_quality(lat: float, lon: float):
    station_name, distance_km = get_nearest_station(lat, lon)
    result = get_station_payload(station_name)
    
    if not result:
        raise HTTPException(status_code=404, detail="Data not found for nearest station.")
        
    latest_data, predictions = result
    
    aqi_val = latest_data.get('AQI', 0)
    primary_pollutant = latest_data.get('Highest Pollutant', 'PM2.5')
    risk_level, personal_prevention = get_health_intelligence(aqi_val)
    
    return {
        "location": {
            "nearest_station": station_name,
            "distance_km": round(distance_km, 2),
            "city": latest_data.get('City', 'Unknown'),
            "state": latest_data.get('State', 'Unknown')
        },
        "current_data": {
            "aqi": aqi_val,
            "pm25": latest_data.get('PM2.5 (ug/m3)', 'N/A'),
            "pm10": latest_data.get('PM10 (ug/m3)', 'N/A'),
            "primary_pollutant": primary_pollutant,
            "date_recorded": str(latest_data.get('Date', 'N/A'))
        },
        "intelligence": {
            "primary_cause": CAUSES.get(primary_pollutant, "General urban pollution mix."),
            "health_risk_level": risk_level,
            "preventive_measure": personal_prevention,
            "reduction_recommendations": REDUCTION_TIPS.get(primary_pollutant, ["Increase local green cover.", "Reduce emissions."])
        },
        "ml_predictions_1yr": predictions 
    }

# --- ✨ NEW ROUTE: Top Polluted Locations in India ---
@router.get("/api/top-locations")
def fetch_top_polluted(limit: int = 5):
    """Returns the top N most polluted locations in India right now."""
    top_data = get_top_polluted(limit)
    return {
        "title": f"Top {limit} Most Polluted Locations",
        "data": top_data
    }