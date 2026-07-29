from sqlalchemy.orm import Session
from app.models import Station, HistoricAQI
import math

def haversine(lat1, lon1, lat2, lon2):
    lat_rad, lon_rad = math.radians(lat1), math.radians(lon1)
    ulat_rad, ulon_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat_rad - ulat_rad
    dlon = lon_rad - ulon_rad
    a = math.sin(dlat / 2)**2 + math.cos(ulat_rad) * math.cos(lat_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c

def find_nearest_station_with_data(lat: float, lon: float, db: Session):
    stations = db.query(Station).all()
    if not stations:
        return {"data_unavailable": True}

    nearest_station = None
    min_dist = float('inf')
    
    # 1. Find absolute nearest station to determine the assumed state
    for st in stations:
        dist = haversine(st.latitude, st.longitude, lat, lon)
        if dist < min_dist:
            min_dist = dist
            nearest_station = st
            
    if not nearest_station:
        return {"data_unavailable": True}
        
    assumed_state = nearest_station.state
    
    # 2. Check if the nearest station has data
    has_data = db.query(HistoricAQI).filter_by(station_id=nearest_station.id).first() is not None
    
    if has_data:
        # Distance > 10km implies a fallback even if it's the absolute nearest
        is_fallback = min_dist > 10.0
        return {
            "station": nearest_station,
            "distance_km": round(min_dist, 1),
            "is_fallback": is_fallback,
            "data_unavailable": False
        }
        
    # 3. If nearest station has no data, search within the same state for the closest station WITH data
    same_state_stations = [st for st in stations if st.state == assumed_state and st.id != nearest_station.id]
    
    fallback_station = None
    fallback_min_dist = float('inf')
    
    for st in same_state_stations:
        st_has_data = db.query(HistoricAQI).filter_by(station_id=st.id).first() is not None
        if st_has_data:
            dist = haversine(st.latitude, st.longitude, lat, lon)
            if dist < fallback_min_dist:
                fallback_min_dist = dist
                fallback_station = st
                
    if fallback_station:
        return {
            "station": fallback_station,
            "distance_km": round(fallback_min_dist, 1),
            "is_fallback": True,
            "data_unavailable": False
        }
        
    # 4. If no station in the same state has data
    return {"data_unavailable": True}

def find_nearest_station(lat: float, lon: float, db: Session):
    stations = db.query(Station).all()
    if not stations:
        return None
        
    nearest_station = None
    min_dist = float('inf')
    
    for st in stations:
        dist = haversine(st.latitude, st.longitude, lat, lon)
        if dist < min_dist:
            min_dist = dist
            nearest_station = st
            
    return nearest_station.name if nearest_station else None