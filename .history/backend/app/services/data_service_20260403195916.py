import pandas as pd
import numpy as np

# Load processed data into memory once when server starts
STATIONS_DF = pd.read_csv('../data/processed/stations.csv')
AQI_DF = pd.read_csv('../data/processed/cleaned_data.csv')
PREDICTIONS_DF = pd.read_csv('../data/processed/predictions_1yr.csv')

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points."""
    R = 6371 # Earth radius in km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def get_nearest_station(lat, lon):
    distances = haversine(lat, lon, STATIONS_DF['Latitude'].values, STATIONS_DF['Longitude'].values)
    nearest_idx = np.argmin(distances)
    return STATIONS_DF.iloc[nearest_idx]['Monitoring Station']

def get_station_data(station_name):
    # Get latest historical data
    station_history = AQI_DF[AQI_DF['Monitoring Station'] == station_name]
    latest_row = station_history.iloc[-1]
    
    # Get 12-month predictions
    preds = PREDICTIONS_DF[PREDICTIONS_DF['Monitoring Station'] == station_name]['Predicted_AQI'].tolist()
    
    return latest_row, preds