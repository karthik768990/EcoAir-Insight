def get_health_risk_category(aqi: int) -> tuple:
    """Get health risk category based on AQI value."""
    if aqi <= 50:
        return "Good", "Enjoy outdoor activities. Air quality is satisfactory."
    elif aqi <= 100:
        return "Moderate", "Sensitive groups should limit prolonged outdoor exertion."
    elif aqi <= 200:
        return "Poor", "Wear an N95 mask outdoors. Run air purifiers inside."
    elif aqi <= 300:
        return "Very Poor", "Avoid outdoor physical activity. Wear respiratory protection."
    else:
        return "Severe", "Avoid all outdoor activities. Keep windows closed."


def get_preventive_measures(primary_pollutant: str) -> str:
    """Get preventive measures for primary pollutant."""
    measures = {
        "PM2.5": "Use HEPA filters. Avoid outdoor exercise. Sources: Vehicle exhaust and industrial emissions.",
        "PM10": "Wear dust mask. Keep doors/windows closed. Sources: Construction dust and road dust.",
        "O3": "Avoid strenuous exercise during peak hours. Vulnerable groups should limit outdoor exposure.",
        "NO2": "Ensure good ventilation indoors. Avoid areas near heavy traffic.",
        "SO2": "Avoid outdoor exposure during pollution peaks. Industrial areas should be avoided.",
        "CO": "Avoid roads with heavy traffic. Use public transport."
    }
    
    return measures.get(primary_pollutant, "Limit outdoor exposure and use air purification indoors.")


def get_pollution_causes(primary_pollutant: str) -> str:
    """Get information about pollution sources."""
    causes = {
        "PM2.5": "Vehicle exhaust, industrial emissions, biomass burning, and road dust.",
        "PM10": "Construction dust, road dust, windblown soil, and industrial operations.",
        "O3": "Formed by reactions between NOx and VOCs in sunlight.",
        "NO2": "Released from vehicle emissions and power plants.",
        "SO2": "Released from burning fossil fuels in power plants and refineries.",
        "CO": "Released from incomplete combustion in vehicles and heating systems."
    }
    
    return causes.get(primary_pollutant, "Urban and industrial pollution sources.")
