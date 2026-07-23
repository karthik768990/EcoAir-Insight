from sqlalchemy.orm import Session
from app.models import Station, HistoricAQI
import re

def normalize(text):
    if not text:
        return ""
    text = str(text).lower().strip()
    return re.sub(r"[^a-z0-9 ]", "", text)

def get_current_aqi(station_name: str, db: Session):
    print("\n AQI SERVICE CALLED")
    print("Input station:", station_name)

    station_norm = normalize(station_name)
    
    # EXACT MATCH
    station = db.query(Station).filter_by(name_norm=station_norm).first()
    
    # PARTIAL MATCH
    if not station:
        station = db.query(Station).filter(Station.name_norm.like(f"%{station_norm}%")).first()
        
    # CITY MATCH
    if not station:
        words = station_norm.split()
        possible_city = words[-1] if words else ""
        if possible_city:
            station = db.query(Station).filter(Station.city.ilike(f"%{possible_city}%")).first()
            
    # FALLBACK
    if not station:
        station = db.query(Station).first() # Global fallback to whatever first station
        print("Using global fallback station:", station.name if station else "None")

    if not station:
        return {}

    latest_history = db.query(HistoricAQI).filter_by(station_id=station.id).order_by(HistoricAQI.date.desc()).first()

    if not latest_history:
        return {}

    result = {
        "aqi": latest_history.aqi,
        "pm25": latest_history.pm25,
        "pm10": latest_history.pm10,
        "no2": latest_history.no2,
        "so2": latest_history.so2,
        "co": latest_history.co,
        "ozone": latest_history.ozone,
        "temp": latest_history.temp, # Actual temperature, no fake modifications
        "rh": latest_history.rh,
        "ws": latest_history.ws,
        "city": station.city,
        "state": station.state
    }

    print("FINAL OUTPUT:", result)
    return result