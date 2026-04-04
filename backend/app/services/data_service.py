import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict, List
from services.location_service import haversine

STATIONS_DF = None
AQI_DF = None
PREDICTIONS_DF = None
DATA_LOADED = False


def _get_data_paths():
    from core.config import STATIONS_CSV, AQI_CSV, PREDICTIONS_CSV
    return STATIONS_CSV, AQI_CSV, PREDICTIONS_CSV


def load_data():
    global STATIONS_DF, AQI_DF, PREDICTIONS_DF, DATA_LOADED
    
    try:
        stations_path, aqi_path, predictions_path = _get_data_paths()
        
        if not stations_path.exists():
            raise FileNotFoundError(f"Stations data not found: {stations_path}")
        if not aqi_path.exists():
            raise FileNotFoundError(f"AQI data not found: {aqi_path}")
        if not predictions_path.exists():
            raise FileNotFoundError(f"Predictions data not found: {predictions_path}")
        
        print(f"Loading stations data...")
        STATIONS_DF = pd.read_csv(stations_path)
        
        print(f"Loading AQI data...")
        AQI_DF = pd.read_csv(aqi_path)
        
        print(f"Loading predictions...")
        PREDICTIONS_DF = pd.read_csv(predictions_path)
        
        DATA_LOADED = True
        print("✓ All data loaded successfully")
        
    except Exception as e:
        DATA_LOADED = False
        print(f"Error loading data: {str(e)}")
        raise RuntimeError(f"Failed to load data: {str(e)}")


def is_data_loaded() -> bool:
    return DATA_LOADED


def get_nearest_station(lat: float, lon: float) -> Optional[str]:
    if not DATA_LOADED or STATIONS_DF is None or len(STATIONS_DF) == 0:
        raise RuntimeError("Data not loaded. Call load_data() first.")
    
    try:
        distances = haversine(
            lat, lon,
            STATIONS_DF['Latitude'].values,
            STATIONS_DF['Longitude'].values
        )
        
        nearest_idx = np.argmin(distances)
        nearest_distance = distances[nearest_idx]
        
        if nearest_distance > 100:
            print(f"Warning: Nearest station is {nearest_distance:.2f} km away")
        
        return STATIONS_DF.iloc[nearest_idx]['Monitoring Station']
    
    except Exception as e:
        raise RuntimeError(f"Error finding nearest station: {str(e)}")


def get_station_data(station_name: str) -> Tuple[Optional[Dict], List[float]]:
    if not DATA_LOADED:
        raise RuntimeError("Data not loaded. Call load_data() first.")
    
    try:
        station_history = AQI_DF[AQI_DF['Monitoring Station'] == station_name]
        
        if len(station_history) == 0:
            raise ValueError(f"No data found for station: {station_name}")
        
        latest_row = station_history.iloc[-1]
        
        station_preds = PREDICTIONS_DF[PREDICTIONS_DF['Monitoring Station'] == station_name]
        
        if len(station_preds) == 0:
            predictions = []
        else:
            station_preds = station_preds.sort_values('Month_Ahead', ascending=True)
            predictions = station_preds['Predicted_AQI'].tolist()
        
        return latest_row.to_dict(), predictions
    
    except Exception as e:
        raise RuntimeError(f"Error fetching station data: {str(e)}")