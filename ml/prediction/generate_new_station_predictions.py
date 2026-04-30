import pandas as pd
import numpy as np
import os
import re

# Paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
predictions_path = os.path.join(base_dir, "data", "processed", "predictions_5yr_advanced.csv")
new_stations_path = os.path.join(base_dir, "data", "processed", "new_stations_data.csv")
old_stations_path = os.path.join(base_dir, "data", "processed", "stations.csv")

def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    return re.sub(r"[^a-z0-9 ]", "", text)

# Load data
preds_df = pd.read_csv(predictions_path)
new_df = pd.read_csv(new_stations_path)
old_df = pd.read_csv(old_stations_path)

# Prepare old stations
old_df["latitude"] = pd.to_numeric(old_df["latitude"], errors="coerce")
old_df["longitude"] = pd.to_numeric(old_df["longitude"], errors="coerce")
old_df = old_df.dropna(subset=["latitude", "longitude"])
old_df["station_norm"] = old_df["monitoring station"].apply(normalize)

# Prepare predictions
preds_df["station_norm"] = preds_df["Monitoring Station"].apply(normalize)
original_preds = preds_df.copy()

# Filter old stations to ONLY those that have predictions
valid_old_df = old_df[old_df["station_norm"].isin(original_preds["station_norm"])].copy()

# Prepare new stations
unique_new_stations = new_df.drop_duplicates(subset=["STATION     NAME"]).copy()
unique_new_stations["Latitude"] = pd.to_numeric(unique_new_stations["Latitude"], errors="coerce")
unique_new_stations["Longitude"] = pd.to_numeric(unique_new_stations["Longitude"], errors="coerce")
unique_new_stations = unique_new_stations.dropna(subset=["Latitude", "Longitude"])

new_preds_list = []
added_count = 0

for _, row in unique_new_stations.iterrows():
    new_name = row["STATION     NAME"]
    new_lat = row["Latitude"]
    new_lon = row["Longitude"]
    
    new_norm = normalize(new_name)
    
    # Check if already in predictions
    if new_norm in preds_df["station_norm"].values:
        continue
        
    # Find nearest valid old station (one that definitely has predictions)
    latitudes = valid_old_df["latitude"].values
    longitudes = valid_old_df["longitude"].values
    distances = np.sqrt((latitudes - new_lat)**2 + (longitudes - new_lon)**2)
    nearest_idx = np.argmin(distances)
    nearest_old_station = valid_old_df.iloc[nearest_idx]
    
    # Extract predictions for nearest old station
    nearest_norm = nearest_old_station["station_norm"]
    nearest_preds = original_preds[original_preds["station_norm"] == nearest_norm].copy()
    
    if not nearest_preds.empty:
        # Swap the name to the new station
        nearest_preds["Monitoring Station"] = new_name
        nearest_preds["station_norm"] = new_norm
        new_preds_list.append(nearest_preds)
        added_count += 1

if new_preds_list:
    new_preds_df = pd.concat(new_preds_list, ignore_index=True)
    final_preds_df = pd.concat([preds_df, new_preds_df], ignore_index=True)
    
    if "station_norm" in final_preds_df.columns:
        final_preds_df = final_preds_df.drop(columns=["station_norm"])
        
    final_preds_df.to_csv(predictions_path, index=False)
    print(f"Successfully appended 5-year predictions for {added_count} new stations!")
else:
    print("No new predictions needed.")
