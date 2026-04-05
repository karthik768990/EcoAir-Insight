import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

print("Loading ML Data into Backend...")

DATA_DIR = os.path.join(BASE_DIR,"ml/data/cleaned_data")
# Absolute path to where your ML model saved the data

try:
    STATIONS_DF = pd.read_csv(os.path.join(DATA_DIR, 'stations.csv'))
    AQI_DF = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_data.csv'))
    PREDICTIONS_DF = pd.read_csv(os.path.join(DATA_DIR, 'predictions_1yr.csv'))
    
    # Ensure Date is a proper datetime object for sorting
    AQI_DF['Date'] = pd.to_datetime(AQI_DF['Date'])
    print("✅ Data loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ ERROR: Could not find data files. Make sure the paths are correct. {e}")

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def get_nearest_station(user_lat, user_lon):
    distances = haversine_distance(user_lat, user_lon, STATIONS_DF['Latitude'].values, STATIONS_DF['Longitude'].values)
    nearest_idx = np.argmin(distances)
    nearest_station = STATIONS_DF.iloc[nearest_idx]
    return nearest_station['Monitoring Station'], distances[nearest_idx]

def get_station_payload(station_name):
    station_history = AQI_DF[AQI_DF['Monitoring Station'] == station_name]
    if station_history.empty: return None
    
    # Get the latest row and fill missing values so JSON doesn't break
    latest_row = station_history.iloc[-1].fillna("N/A").to_dict()
    
    station_preds = PREDICTIONS_DF[PREDICTIONS_DF['Monitoring Station'] == station_name]
    predictions_list = station_preds['Predicted_AQI'].tolist() if not station_preds.empty else []
    
    return latest_row, predictions_list

# ✨ NEW FUNCTION: Get the Top Polluted Places in India right now
def get_top_polluted(limit=5):
    # Sort chronologically, then keep only the LAST (most recent) record for each station
    latest_snapshot = AQI_DF.sort_values('Date').drop_duplicates('Monitoring Station', keep='last')
    
    # Find the top 'limit' stations with the highest AQI
    top_stations = latest_snapshot.nlargest(limit, 'AQI')
    
    results = []
    for _, row in top_stations.iterrows():
        # Grab predictions for these top places too
        preds = PREDICTIONS_DF[PREDICTIONS_DF['Monitoring Station'] == row['Monitoring Station']]['Predicted_AQI'].tolist()
        results.append({
            "station": row['Monitoring Station'],
            "city": row['City'],
            "state": row['State'],
            "current_aqi": row['AQI'],
            "primary_pollutant": row['Highest Pollutant'],
            "date": row['Date'].strftime('%Y-%m-%d'),
            "predictions_1yr": preds
        })
    return results