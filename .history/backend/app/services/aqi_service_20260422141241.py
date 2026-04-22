import pandas as pd
import os
import re

# =============================
# LOAD DATA
# =============================
current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/cleaned_data.csv")
)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"AQI file not found at: {data_path}")

df = pd.read_csv(data_path)

df.columns = df.columns.str.strip()

# Normalize names
df.rename(columns={
    "Monitoring Station": "station",
    "State": "state",
    "City": "city",
    "Date": "date",
    "AQI": "aqi",
    "PM2.5 (ug/m3)": "pm2.5",
    "PM10 (ug/m3)": "pm10"
}, inplace=True)

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

        # Extract city from station name
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
        if col in station_data:
            return get_latest(station_data[col])
        return None

    aqi = get_latest(station_data["aqi"])
    pm25 = get_latest(station_data["pm2.5"])
    pm10 = get_latest(station_data["pm10"])
    city = get_latest(station_data["city"])
    state = get_latest(station_data["state"])

    # =============================
    # OPTIONAL NEW DATA (SAFE)
    # =============================
    

    result = {
    "aqi": float(aqi) if aqi else None,
    "pm25": float(pm25) if pm25 else None,
    "pm10": float(pm10) if pm10 else None,

    # 🔥 SMART FETCH (not just latest row)
    "no2": safe_col("no2"),
    "so2": safe_col("so2"),
    "co": safe_col("co"),
    "ozone": safe_col("ozone"),

    "temp": safe_col("temp"),
    "rh": safe_col("rh"),
    "ws": safe_col("ws"),

    "city": city,
    "state": state
    }
    print("✅ FINAL OUTPUT:", result)

    return result   