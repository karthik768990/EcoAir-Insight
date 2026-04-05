import pandas as pd
import numpy as np
from typing import Tuple, Optional, Dict, List
from services.location_service import haversine
import joblib

# Data loaded from ml/data/processed/ (ML folder)
STATIONS_DF = None
AQI_DF = None
PREDICTIONS_DF = None  # 5-year predictions from ML model
ML_MODEL = None  # Trained HistGradientBoostingRegressor
DATA_LOADED = False


def _get_data_paths():
    from core.config import STATIONS_CSV, AQI_CSV, PREDICTIONS_CSV, MODEL_PATH
    return STATIONS_CSV, AQI_CSV, PREDICTIONS_CSV, MODEL_PATH


def load_data():
    global STATIONS_DF, AQI_DF, PREDICTIONS_DF, ML_MODEL, DATA_LOADED
    
    try:
        stations_path, aqi_path, predictions_path, model_path = _get_data_paths()
        
        if not stations_path.exists():
            raise FileNotFoundError(f"Stations data not found: {stations_path}")
        if not aqi_path.exists():
            raise FileNotFoundError(f"AQI data not found: {aqi_path}")
        if not predictions_path.exists():
            raise FileNotFoundError(f"Predictions data not found: {predictions_path}")
        
        print(f"Loading stations data from {stations_path.parent}...")
        STATIONS_DF = pd.read_csv(stations_path)
        # Ensure latitude and longitude are numeric
        STATIONS_DF['Latitude'] = pd.to_numeric(STATIONS_DF['Latitude'], errors='coerce')
        STATIONS_DF['Longitude'] = pd.to_numeric(STATIONS_DF['Longitude'], errors='coerce')
        # Remove any rows with NULL coordinates
        STATIONS_DF = STATIONS_DF.dropna(subset=['Latitude', 'Longitude'])
        
        print(f"Loading AQI data...")
        AQI_DF = pd.read_csv(aqi_path)
        
        print(f"Loading 5-year predictions...")
        PREDICTIONS_DF = pd.read_csv(predictions_path)
        
        # Load ML model if available
        if model_path.exists() and model_path.stat().st_size > 0:
            try:
                print(f"Loading ML model from {model_path}...")
                ML_MODEL = joblib.load(model_path)
                print(f"[OK] ML model loaded successfully")
            except Exception as model_err:
                print(f"[WARNING] Failed to load ML model: {model_err}")
                ML_MODEL = None
        else:
            if model_path.exists():
                print(f"[WARNING] ML model file is empty or invalid at {model_path}")
            else:
                print(f"[WARNING] ML model not found at {model_path}")
            ML_MODEL = None
        
        DATA_LOADED = True
        print("[OK] All data and models loaded successfully")
        
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


def get_ml_model():
    """Get loaded ML model for predictions."""
    if not DATA_LOADED:
        raise RuntimeError("Data not loaded. Call load_data() first.")
    if ML_MODEL is None:
        raise RuntimeError("ML model not available. Ensure saved_model.pkl exists in ml/models/")
    return ML_MODEL