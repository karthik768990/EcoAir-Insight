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
stations_df["latitude"] = pd.to_numeric(stations_df["latitude"], errors="coerce")
stations_df["longitude"] = pd.to_numeric(stations_df["longitude"], errors="coerce")

# Optional: drop bad rows
stations_df = stations_df.dropna(subset=["latitude", "longitude"])

# 🔥 Load new geocoded stations if they exist
new_data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/new_stations_data.csv")
)
if os.path.exists(new_data_path):
    try:
        new_df = pd.read_csv(new_data_path)
        new_stations = pd.DataFrame({
            "monitoring station": new_df["STATION     NAME"],
            "latitude": pd.to_numeric(new_df["Latitude"], errors="coerce"),
            "longitude": pd.to_numeric(new_df["Longitude"], errors="coerce"),
        })
        new_stations = new_stations.dropna(subset=["latitude", "longitude"])
        new_stations = new_stations.drop_duplicates(subset=["monitoring station"])
        stations_df = pd.concat([stations_df, new_stations], ignore_index=True)
    except Exception as e:
        print("Error loading new stations:", e)


def find_nearest_station(lat, lon):
    latitudes = stations_df["latitude"].values
    longitudes = stations_df["longitude"].values

    distances = np.sqrt((latitudes - lat)**2 + (longitudes - lon)**2)

    idx = np.argmin(distances)

    return stations_df.iloc[idx]["monitoring station"]