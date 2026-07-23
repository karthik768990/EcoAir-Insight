from sqlalchemy.orm import Session
from app.models import Station, Prediction
import re

def normalize(text):
    if not text: return ""
    return re.sub(r"[^a-z0-9 ]", "", str(text).lower().strip())

def get_prediction(station_name: str, db: Session):
    station_norm = normalize(station_name)
    
    # Try exact match
    station = db.query(Station).filter_by(name_norm=station_norm).first()
    
    # Try partial
    if not station:
        station = db.query(Station).filter(Station.name_norm.like(f"%{station_norm}%")).first()
        
    if not station:
        return []
        
    preds = db.query(Prediction).filter_by(station_id=station.id).order_by(Prediction.month_ahead).all()
    
    return [
        {
            "month": p.month_ahead,
            "aqi": p.predicted_aqi,
            "lower": p.lower_bound,
            "upper": p.upper_bound
        }
        for p in preds
    ]