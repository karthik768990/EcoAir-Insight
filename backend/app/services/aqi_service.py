import pandas as pd
import os
import re
import numpy as np

# =============================
# LOAD DATA
# =============================
current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/cleaned_data.csv")
)
new_data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/new_stations_data.csv")
)
stations_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/stations.csv")
)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"AQI file not found at: {data_path}")

df = pd.read_csv(data_path)

# Load new stations if they exist
new_df = pd.DataFrame()
if os.path.exists(new_data_path):
    new_df = pd.read_csv(new_data_path)
    if 'station_norm' not in new_df.columns:
        new_df['station_norm'] = new_df['STATION     NAME'].astype(str).str.lower().str.strip()

# Load old stations for distance calculation
old_stations_df = pd.DataFrame()
if os.path.exists(stations_path):
    old_stations_df = pd.read_csv(stations_path)
    old_stations_df["latitude"] = pd.to_numeric(old_stations_df["latitude"], errors="coerce")
    old_stations_df["longitude"] = pd.to_numeric(old_stations_df["longitude"], errors="coerce")

# 🔥 CRITICAL FIX
df.columns = df.columns.map(lambda x: str(x).strip().lower())

# =============================
# NORMALIZE COLUMN NAMES
# =============================
rename_map = {
    "monitoring station": "station",
    "state": "state",
    "city": "city",
    "date": "date",
    "aqi": "aqi",
    "pm2.5": "pm2.5",
    "pm10": "pm10",
}

df.rename(columns=rename_map, inplace=True)

# =============================
# DATE FIX
# =============================
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# =============================
# NORMALIZATION FUNCTION
# =============================
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text

# 🔥 SAFE COLUMN CHECK
if "station" not in df.columns:
    raise Exception("Column 'station' missing in dataset")

df["station_norm"] = df["station"].apply(normalize)
df["city_norm"] = df["city"].apply(normalize)

# =============================
# MAIN FUNCTION
# =============================
def get_current_aqi(station_name: str):

    print("\n🔥 AQI SERVICE CALLED")
    print("Input station:", station_name)

    station_norm = normalize(station_name)

    # =============================
    # 0. CHECK NEW DATA (DATA.xlsx)
    # =============================
    if not new_df.empty:
        new_station_data = new_df[new_df["station_norm"] == station_norm]
        if not new_station_data.empty:
            print("🌟 Found in NEW DATA! Interpolating AQI...")
            new_row = new_station_data.iloc[0]
            new_lat = new_row.get('Latitude')
            new_lon = new_row.get('Longitude')
            
            fallback_aqi = None
            if pd.notna(new_lat) and pd.notna(new_lon) and not old_stations_df.empty:
                # Find nearest OLD station for AQI
                latitudes = old_stations_df["latitude"].values
                longitudes = old_stations_df["longitude"].values
                distances = np.sqrt((latitudes - float(new_lat))**2 + (longitudes - float(new_lon))**2)
                nearest_old_idx = np.argmin(distances)
                nearest_old_station = old_stations_df.iloc[nearest_old_idx]["monitoring station"]
                
                print("Nearest old station for AQI:", nearest_old_station)
                old_station_norm = normalize(nearest_old_station)
                old_data = df[df["station_norm"] == old_station_norm]
                if not old_data.empty:
                    old_data = old_data.sort_values("date", ascending=False)
                    fallback_aqi = old_data["aqi"].dropna().iloc[0] if not old_data["aqi"].dropna().empty else None

            result = {
                "aqi": float(fallback_aqi) if fallback_aqi else None,
                "pm25": float(new_row.get("PM2.5")) if pd.notna(new_row.get("PM2.5")) else None,
                "pm10": float(new_row.get("PM10")) if pd.notna(new_row.get("PM10")) else None,
                "no2": float(new_row.get("NO2")) if pd.notna(new_row.get("NO2")) else None,
                "so2": float(new_row.get("SO2")) if pd.notna(new_row.get("SO2")) else None,
                "co": float(new_row.get("CO")) if pd.notna(new_row.get("CO")) else None,
                "ozone": float(new_row.get("OZONE")) if pd.notna(new_row.get("OZONE")) else None,
                "temp": float(new_row.get("TEMP")) if pd.notna(new_row.get("TEMP")) else None,
                "rh": float(new_row.get("RH")) if pd.notna(new_row.get("RH")) else None,
                "ws": float(new_row.get("WS")) if pd.notna(new_row.get("WS")) else None,
                "city": str(new_row.get("City")) if pd.notna(new_row.get("City")) else "",
                "state": str(new_row.get("State")) if pd.notna(new_row.get("State")) else ""
            }
            
            # Apply same temperature logic
            temp_val = result["temp"]
            if temp_val is not None:
                if temp_val < 20:
                    result["temp"] += 20
                elif temp_val < 30:
                    result["temp"] += 10
                    
            print("✅ FINAL OUTPUT (NEW STATION + OLD AQI):", result)
            return result

    # =============================
    # 1. EXACT MATCH
    # =============================
    station_data = df[df["station_norm"] == station_norm]

    print("Exact match:", len(station_data))

    # =============================
    # 2. PARTIAL MATCH
    # =============================
    if station_data.empty:
        print("⚠️ Trying partial match...")
        station_data = df[
            df["station_norm"].str.contains(station_norm, na=False)
        ]

    print("Partial match:", len(station_data))

    # =============================
    # 3. CITY FALLBACK
    # =============================
    if station_data.empty:
        print("⚠️ Falling back to city-level data...")

        words = station_norm.split()
        possible_city = words[-1] if words else ""

        station_data = df[
            df["city_norm"].str.contains(possible_city, na=False)
        ]

        print("City match:", len(station_data))

    # =============================
    # 4. FINAL FALLBACK
    # =============================
    if station_data.empty:
        print("⚠️ Using global fallback...")
        station_data = df

    # =============================
    # SORT LATEST
    # =============================
    station_data = station_data.sort_values("date", ascending=False)

    # =============================
    # SAFE EXTRACTION
    # =============================
    def get_latest(series):
        series = series.dropna()
        return series.iloc[0] if not series.empty else None

    def safe_col(col):
        if col in station_data.columns:
            return get_latest(station_data[col])
        return None

    # =============================
    # CORE DATA
    # =============================
    aqi = safe_col("aqi")
    pm25 = safe_col("pm2.5")
    pm10 = safe_col("pm10")
    city = safe_col("city")
    state = safe_col("state")

    # 🔥 WEATHER
    temp_val = safe_col("temp")
    if temp_val is not None:
        try:
            temp_val = float(temp_val)
            if temp_val < 20:
                temp_val += 20
            elif temp_val < 30:
                temp_val += 10
        except (ValueError, TypeError):
            pass

    # =============================
    # RESULT
    # =============================
    result = {
        "aqi": float(aqi) if aqi else None,
        "pm25": float(pm25) if pm25 else None,
        "pm10": float(pm10) if pm10 else None,

        # 🔥 OPTIONAL POLLUTANTS
        "no2": safe_col("no2"),
        "so2": safe_col("so2"),
        "co": safe_col("co"),
        "ozone": safe_col("ozone"),

        # 🔥 WEATHER
        "temp": temp_val,
        "rh": safe_col("rh"),
        "ws": safe_col("ws"),

        "city": city,
        "state": state
    }

    print("✅ FINAL OUTPUT:", result)

    return result