import pandas as pd
import numpy as np
import re
import os

def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text

cleaned_path = '../../../ml/data/processed/cleaned_data.csv'
stations_path = '../../../ml/data/processed/stations.csv'
new_stations_path = '../../../ml/data/processed/new_stations_data.csv'

df = pd.read_csv(cleaned_path)
df.columns = df.columns.map(lambda x: str(x).strip().lower())
rename_map = {
    "monitoring station": "station",
    "state": "state",
    "city": "city",
    "date": "date",
    "aqi": "aqi"
}
df.rename(columns=rename_map, inplace=True)

df["station_norm"] = df["station"].apply(normalize)
df["city_norm"] = df["city"].apply(normalize)

stations_df = pd.read_csv(stations_path)
stations_df["latitude"] = pd.to_numeric(stations_df["latitude"], errors="coerce")
stations_df["longitude"] = pd.to_numeric(stations_df["longitude"], errors="coerce")
stations_df = stations_df.dropna(subset=["latitude", "longitude"])

functional_old = []
for _, row in stations_df.iterrows():
    name = row["monitoring station"]
    lat = row["latitude"]
    lon = row["longitude"]
    
    station_norm = normalize(name)
    
    # 1. Exact
    station_data = df[df["station_norm"] == station_norm]
    match_type = "Exact"
    
    # 2. Partial
    if station_data.empty:
        station_data = df[df["station_norm"].str.contains(station_norm, na=False)]
        match_type = "Partial"
        
    # 3. City
    if station_data.empty:
        words = station_norm.split()
        possible_city = words[-1] if words else ""
        if possible_city:
            station_data = df[df["city_norm"].str.contains(possible_city, na=False)]
            match_type = "City"
    
    if not station_data.empty:
        functional_old.append((name, lat, lon, match_type))

# new stations
new_df = pd.DataFrame()
functional_new = []
if os.path.exists(new_stations_path):
    new_df = pd.read_csv(new_stations_path)
    for _, row in new_df.iterrows():
        name = row["STATION     NAME"]
        lat = pd.to_numeric(row["Latitude"], errors="coerce")
        lon = pd.to_numeric(row["Longitude"], errors="coerce")
        if pd.notna(lat) and pd.notna(lon):
            functional_new.append((name, lat, lon, "New Station Data"))

print(f"Found {len(functional_old)} functional old stations.")
print(f"Found {len(functional_new)} functional new stations.")

out_path = r'C:\Users\Karthik Tamarapalli\.gemini\antigravity\brain\664ca33b-2000-4220-8e8b-d254fb9f4eb4\functional_stations.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write("# Functional Locations in EcoAir-Insight\n\n")
    f.write("These are the locations that will successfully return data without hitting the global fallback (which returns the AQI of 102 from Pune).\n\n")
    
    f.write("## New Stations\n")
    f.write("These stations pull their primary data from the new dataset (DATA.xlsx). If they can't find a local historic station for AQI interpolation, they will fallback but their other metrics (PM2.5, NO2, etc) will still be specific to the station.\n\n")
    f.write("| Station Name | Latitude | Longitude | Match Type |\n")
    f.write("|--------------|----------|-----------|------------|\n")
    for name, lat, lon, mtype in functional_new:
        f.write(f"| {name} | {lat} | {lon} | {mtype} |\n")
        
    f.write("\n## Historic Stations\n")
    f.write("These stations successfully match with the historic `cleaned_data.csv` using Exact, Partial, or City matching.\n\n")
    f.write("| Station Name | Latitude | Longitude | Match Type |\n")
    f.write("|--------------|----------|-----------|------------|\n")
    for name, lat, lon, mtype in functional_old:
        f.write(f"| {name} | {lat} | {lon} | {mtype} |\n")

print(f"Generated {out_path}")
