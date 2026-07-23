import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "backend"))

from app.models import Station, HistoricAQI, Prediction
from app.database import engine, Base

Session = sessionmaker(bind=engine)

def normalize(text):
    import re
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    return re.sub(r"[^a-z0-9 ]", "", text)

def migrate_stations(session):
    print("Migrating stations...")
    old_stations_path = os.path.join(BASE_DIR, "ml/data/processed/stations.csv")
    new_stations_path = os.path.join(BASE_DIR, "ml/data/processed/new_stations_data.csv")

    stations_dict = {}

    # Load old stations
    if os.path.exists(old_stations_path):
        df_old = pd.read_csv(old_stations_path)
        for _, row in df_old.iterrows():
            name = row.get("monitoring station", row.get("Monitoring Station"))
            if pd.isna(name): continue
            norm_name = normalize(name)
            if norm_name not in stations_dict:
                stations_dict[norm_name] = {
                    "name": name,
                    "name_norm": norm_name,
                    "latitude": pd.to_numeric(row.get("latitude", row.get("Latitude")), errors='coerce'),
                    "longitude": pd.to_numeric(row.get("longitude", row.get("Longitude")), errors='coerce'),
                    "city": "",
                    "state": ""
                }

    # Load new stations
    if os.path.exists(new_stations_path):
        df_new = pd.read_csv(new_stations_path)
        for _, row in df_new.iterrows():
            name = row.get("STATION     NAME")
            if pd.isna(name): continue
            norm_name = normalize(name)
            if norm_name not in stations_dict:
                stations_dict[norm_name] = {
                    "name": name,
                    "name_norm": norm_name,
                    "latitude": pd.to_numeric(row.get("Latitude"), errors='coerce'),
                    "longitude": pd.to_numeric(row.get("Longitude"), errors='coerce'),
                    "city": row.get("City", ""),
                    "state": row.get("State", "")
                }
            else:
                # Update city and state if missing
                stations_dict[norm_name]["city"] = row.get("City", "")
                stations_dict[norm_name]["state"] = row.get("State", "")

    # Insert into DB
    for norm_name, data in stations_dict.items():
        if pd.isna(data["latitude"]) or pd.isna(data["longitude"]):
            continue
            
        existing = session.query(Station).filter_by(name_norm=norm_name).first()
        if not existing:
            st = Station(
                name=str(data["name"]),
                name_norm=norm_name,
                city=str(data["city"]) if not pd.isna(data["city"]) else None,
                state=str(data["state"]) if not pd.isna(data["state"]) else None,
                latitude=float(data["latitude"]),
                longitude=float(data["longitude"])
            )
            session.add(st)
    
    session.commit()
    print("Stations migrated successfully.")

def migrate_historical_aqi(session):
    print("Migrating historical AQI data...")
    cleaned_path = os.path.join(BASE_DIR, "ml/data/processed/cleaned_data.csv")
    if not os.path.exists(cleaned_path):
        print("No cleaned_data.csv found.")
        return

    df = pd.read_csv(cleaned_path)
    df.columns = df.columns.map(lambda x: str(x).strip().lower())
    
    # Pre-fetch stations
    stations = {s.name_norm: s.id for s in session.query(Station).all()}
    
    batch_size = 5000
    batch = []
    
    for _, row in df.iterrows():
        station_name = row.get("monitoring station") or row.get("station")
        if pd.isna(station_name): continue
        norm_name = normalize(station_name)
        
        station_id = stations.get(norm_name)
        if not station_id:
            continue
            
        date_val = pd.to_datetime(row.get("date"), errors='coerce')
        if pd.isna(date_val): continue
        
        aqi_record = HistoricAQI(
            station_id=station_id,
            date=date_val.to_pydatetime(),
            aqi=float(row.get("aqi")) if not pd.isna(row.get("aqi")) else None,
            pm25=float(row.get("pm2.5")) if not pd.isna(row.get("pm2.5")) else None,
            pm10=float(row.get("pm10")) if not pd.isna(row.get("pm10")) else None,
            no2=float(row.get("no2")) if not pd.isna(row.get("no2")) else None,
            so2=float(row.get("so2")) if not pd.isna(row.get("so2")) else None,
            co=float(row.get("co")) if not pd.isna(row.get("co")) else None,
            ozone=float(row.get("ozone")) if not pd.isna(row.get("ozone")) else None,
            temp=float(row.get("temp")) if not pd.isna(row.get("temp")) else None,
            rh=float(row.get("rh")) if not pd.isna(row.get("rh")) else None,
            ws=float(row.get("ws")) if not pd.isna(row.get("ws")) else None
        )
        batch.append(aqi_record)
        
        if len(batch) >= batch_size:
            session.bulk_save_objects(batch)
            session.commit()
            batch = []
            
    if batch:
        session.bulk_save_objects(batch)
        session.commit()
        
    print("Historical AQI data migrated successfully.")

def run_migration():
    Base.metadata.create_all(bind=engine)
    session = Session()
    try:
        migrate_stations(session)
        migrate_historical_aqi(session)
    finally:
        session.close()
    print("Database migration complete.")

if __name__ == "__main__":
    run_migration()
