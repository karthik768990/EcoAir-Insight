import pandas as pd
import os
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/stations.csv")
)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Stations file not found at: {data_path}")

stations_df = pd.read_csv(data_path)

# 🔥 FIX: Convert to numeric
stations_df["Latitude"] = pd.to_numeric(stations_df["Latitude"], errors="coerce")
stations_df["Longitude"] = pd.to_numeric(stations_df["Longitude"], errors="coerce")

# Optional: drop bad rows
stations_df = stations_df.dropna(subset=["Latitude", "Longitude"])


def find_nearest_station(lat, lon):
    latitudes = stations_df["Latitude"].values
    longitudes = stations_df["Longitude"].values

    distances = np.sqrt((latitudes - lat)**2 + (longitudes - lon)**2)

    idx = np.argmin(distances)

    return stations_df.iloc[idx]["Monitoring Station"]