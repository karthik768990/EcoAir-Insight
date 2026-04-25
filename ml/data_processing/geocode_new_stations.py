import pandas as pd
import requests
import time
import os
import urllib.parse

def geocode_city(city, state):
    query = f"{city}, {state}, India"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    headers = {"User-Agent": "EcoAir-Insight-Geocoding-Script/1.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        pass
    return None, None

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    raw_dir = os.path.join(base_dir, "ml", "data", "raw_data")
    processed_dir = os.path.join(base_dir, "ml", "data", "processed")

    data_file = os.path.join(raw_dir, "DATA.xlsx")
    coords_file = os.path.join(raw_dir, "MS with lat and Lon.xlsx")
    output_file = os.path.join(processed_dir, "new_stations_data.csv")

    df_data = pd.read_excel(data_file)
    df_coords = pd.read_excel(coords_file)

    df_data['station_norm'] = df_data['STATION     NAME'].astype(str).str.lower().str.strip()
    df_coords['station_norm'] = df_coords['Monitoring Station'].astype(str).str.lower().str.strip()
    df_coords = df_coords.drop_duplicates(subset=['station_norm'])

    merged = pd.merge(df_data, df_coords[['station_norm', 'Latitude', 'Longitude']], on='station_norm', how='left')

    # Find unique stations missing coordinates
    missing_mask = merged['Latitude'].isna()
    unique_missing = merged[missing_mask].drop_duplicates(subset=['station_norm'])
    
    city_cache = {}
    station_coords = {}

    for _, row in unique_missing.iterrows():
        station = row['station_norm']
        city = row['City']
        state = row['State']
        
        if pd.isna(city):
            station_coords[station] = (None, None)
            continue

        cache_key = f"{city}_{state}"
        if cache_key in city_cache:
            lat, lon = city_cache[cache_key]
        else:
            lat, lon = geocode_city(city, state)
            city_cache[cache_key] = (lat, lon)
            time.sleep(1.1)

        station_coords[station] = (lat, lon)

    # Apply coordinates back to the full dataset
    def get_lat(row):
        if pd.notna(row['Latitude']): return row['Latitude']
        return station_coords.get(row['station_norm'], (None, None))[0]

    def get_lon(row):
        if pd.notna(row['Longitude']): return row['Longitude']
        return station_coords.get(row['station_norm'], (None, None))[1]

    merged['Latitude'] = merged.apply(get_lat, axis=1)
    merged['Longitude'] = merged.apply(get_lon, axis=1)

    # Sort descending by date so we have the latest
    if 'Date' in merged.columns:
        merged['Date'] = pd.to_datetime(merged['Date'], errors='coerce')
        merged = merged.sort_values(by='Date', ascending=False)
        
    merged.to_csv(output_file, index=False)

if __name__ == '__main__':
    main()
