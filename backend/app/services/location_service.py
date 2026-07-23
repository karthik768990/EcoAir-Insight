from sqlalchemy.orm import Session
from app.models import Station
import math

def find_nearest_station(lat: float, lon: float, db: Session):
    stations = db.query(Station).all()
    if not stations:
        return None
        
    nearest_station = None
    min_dist = float('inf')
    
    for st in stations:
        # Haversine distance
        lat_rad, lon_rad = math.radians(st.latitude), math.radians(st.longitude)
        ulat_rad, ulon_rad = math.radians(lat), math.radians(lon)
        dlat = lat_rad - ulat_rad
        dlon = lon_rad - ulon_rad
        a = math.sin(dlat / 2)**2 + math.cos(ulat_rad) * math.cos(lat_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = 6371.0 * c
        if dist < min_dist:
            min_dist = dist
            nearest_station = st
            
    return nearest_station.name if nearest_station else None