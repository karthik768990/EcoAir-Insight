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