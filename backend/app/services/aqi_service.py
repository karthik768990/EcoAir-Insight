from typing import Dict, List, Optional
from services.data_service import get_station_data, get_nearest_station
from services.health_service import (
    get_health_risk_category,
    get_preventive_measures,
    get_pollution_causes
)


def get_current_aqi_info(latitude: float, longitude: float) -> Dict:
    """Get current AQI information for a location."""
    try:
        station_name = get_nearest_station(latitude, longitude)
        
        if not station_name:
            raise ValueError("No monitoring station found")
        
        latest_row, predictions = get_station_data(station_name)
        
        if latest_row is None:
            raise ValueError(f"No data for station: {station_name}")
        
        aqi = int(latest_row.get('AQI', 0))
        pm25 = float(latest_row.get('PM2.5 (ug/m3)', 0) or 0)
        pm10 = float(latest_row.get('PM10 (ug/m3)', 0) or 0)
        
        primary_pollutant = determine_primary_pollutant(pm25, pm10, latest_row)
        
        health_risk, suggestion = get_health_risk_category(aqi)
        
        return {
            "location": {"lat": latitude, "lon": longitude},
            "station": station_name,
            "aqi": aqi,
            "pm25": pm25,
            "pm10": pm10,
            "health_risk": health_risk,
            "suggestion": suggestion,
            "primary_pollutant": primary_pollutant,
            "pollution_causes": get_pollution_causes(primary_pollutant),
            "preventive_measures": get_preventive_measures(primary_pollutant)
        }
    
    except Exception as e:
        raise ValueError(f"Error fetching AQI data: {str(e)}")


def get_prediction_data(latitude: float, longitude: float) -> Dict:
    """Get 5-year AQI prediction for a location."""
    try:
        station_name = get_nearest_station(latitude, longitude)
        
        if not station_name:
            raise ValueError("No monitoring station found")
        
        latest_row, predictions = get_station_data(station_name)
        
        if not predictions:
            raise ValueError(f"No predictions for station: {station_name}")
        
        forecast_5_years = predictions[:5] if len(predictions) >= 5 else predictions
        
        return {
            "location": {"lat": latitude, "lon": longitude},
            "station": station_name,
            "forecast_5_years": forecast_5_years
        }
    
    except Exception as e:
        raise ValueError(f"Error fetching predictions: {str(e)}")


def determine_primary_pollutant(pm25: float, pm10: float, row: Dict) -> str:
    """Determine primary pollutant."""
    if pm25 > pm10 * 0.5:
        return "PM2.5"
    elif pm10 > pm25 * 1.5:
        return "PM10"
    
    pollutants = {
        'O3 (ppb)': 'O3',
        'NO2 (ppb)': 'NO2',
        'SO2 (ppb)': 'SO2',
        'CO (ppm)': 'CO'
    }
    
    max_pollutant = 'PM2.5'
    max_value = pm25
    
    for col, pollutant_name in pollutants.items():
        if col in row and row[col]:
            try:
                val = float(row[col])
                if val > max_value:
                    max_value = val
                    max_pollutant = pollutant_name
            except (ValueError, TypeError):
                continue
    
    return max_pollutant
