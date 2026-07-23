from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine
from app.models import Station, HistoricAQI, Prediction
import math

def get_nearest_station(user_lat, user_lon, db: Session):
    # Retrieve all stations to find the nearest (Haversine done in Python for SQLite compatibility)
    stations = db.query(Station).all()
    if not stations:
        return None, float('inf')
        
    nearest_station = None
    min_dist = float('inf')
    
    for st in stations:
        lat_rad, lon_rad = math.radians(st.latitude), math.radians(st.longitude)
        ulat_rad, ulon_rad = math.radians(user_lat), math.radians(user_lon)
        dlat = lat_rad - ulat_rad
        dlon = lon_rad - ulon_rad
        a = math.sin(dlat / 2)**2 + math.cos(ulat_rad) * math.cos(lat_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = 6371.0 * c
        if dist < min_dist:
            min_dist = dist
            nearest_station = st
            
    return nearest_station.name, min_dist

def get_station_payload(station_name: str, db: Session):
    station = db.query(Station).filter_by(name=station_name).first()
    if not station:
        return None
        
    # Get latest history
    latest_history = db.query(HistoricAQI).filter_by(station_id=station.id).order_by(HistoricAQI.date.desc()).first()
    if not latest_history:
        return None
        
    # Format dict
    latest_dict = {
        'Monitoring Station': station.name,
        'City': station.city or 'N/A',
        'State': station.state or 'N/A',
        'Date': latest_history.date.strftime('%Y-%m-%d') if latest_history.date else 'N/A',
        'AQI': latest_history.aqi or 'N/A',
        'PM2.5 (ug/m3)': latest_history.pm25 or 'N/A',
        'PM10 (ug/m3)': latest_history.pm10 or 'N/A',
        'NO2': latest_history.no2 or 'N/A',
        'SO2': latest_history.so2 or 'N/A',
        'CO': latest_history.co or 'N/A',
        'OZONE': latest_history.ozone or 'N/A',
        'Highest Pollutant': 'PM2.5' # simplified for backward compatibility
    }
    
    preds = db.query(Prediction).filter_by(station_id=station.id).order_by(Prediction.month_ahead).all()
    predictions_list = [p.predicted_aqi for p in preds]
    
    return latest_dict, predictions_list

def get_top_polluted(db: Session, limit=5):
    # We use a subquery to find the latest date per station
    subq = db.query(
        HistoricAQI.station_id,
        func.max(HistoricAQI.date).label('maxdate')
    ).group_by(HistoricAQI.station_id).subquery('t2')
    
    # Join to get the actual records
    query = db.query(HistoricAQI, Station).join(
        Station, HistoricAQI.station_id == Station.id
    ).join(
        subq, (HistoricAQI.station_id == subq.c.station_id) & (HistoricAQI.date == subq.c.maxdate)
    ).order_by(HistoricAQI.aqi.desc()).limit(limit)
    
    top_records = query.all()
    results = []
    
    for aqi_rec, st in top_records:
        preds = db.query(Prediction).filter_by(station_id=st.id).order_by(Prediction.month_ahead).all()
        results.append({
            "station": st.name,
            "city": st.city,
            "state": st.state,
            "current_aqi": aqi_rec.aqi,
            "primary_pollutant": "PM2.5", # simplified
            "date": aqi_rec.date.strftime('%Y-%m-%d') if aqi_rec.date else "",
            "predictions_1yr": [p.predicted_aqi for p in preds][:12] # return 1yr (12 months)
        })
        
    return results