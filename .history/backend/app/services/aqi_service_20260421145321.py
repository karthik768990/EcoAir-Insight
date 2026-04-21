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

temp_lookup_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/station_temp_lookup.csv")
)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"AQI file not found at: {data_path}")

df = pd.read_csv(data_path)
df.columns = df.columns.str.strip()

# Normalize column names
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

# ✅ Deduplicate: same station+date may appear 7x from multiple Excel sources
df = df.drop_duplicates(subset=["station", "date"], keep="first")

# =============================
# LOAD TEMPERATURE LOOKUP
# =============================
# station_temp_lookup.csv has one row per station with the latest
# validated temperature (0–48°C). This avoids all fallback/wrong-station issues.
TEMP_LOOKUP = {}

if os.path.exists(temp_lookup_path):
    temp_df = pd.read_csv(temp_lookup_path)
    temp_df.columns = temp_df.columns.str.strip()
    for _, row in temp_df.iterrows():
        station = str(row["Monitoring Station"]).strip()
        temp_val = row.get("Latest_Temp_C")
        if pd.notna(temp_val):
            TEMP_LOOKUP[station] = round(float(temp_val), 1)
    print(f"✅ Temperature lookup loaded: {len(TEMP_LOOKUP)} stations with temp data")
else:
    print(f"⚠️  station_temp_lookup.csv not found at {temp_lookup_path}")
    print("   Temperature will show as null. Run build_temp_lookup.py to fix.")


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
    print("Exact match rows:", len(station_data))

    # =============================
    # 2. PARTIAL MATCH
    # =============================
    if station_data.empty:
        print("⚠️ Trying partial match...")
        station_data = df[df["station_norm"].str.contains(station_norm, na=False)]
        print("Partial match rows:", len(station_data))

    # =============================
    # 3. CITY FALLBACK
    # ✅ FIX: Extract city from the city column of matched rows,
    #         NOT by splitting the station name (which gives agency names like 'dpcc')
    # =============================
    if station_data.empty:
        print("⚠️ Falling back to city-level data...")

        # Try extracting a meaningful city token from station name
        # Station names look like: "Alipur, Delhi - DPCC"
        # We want "Delhi", not "DPCC"
        parts = station_name.replace("-", ",").split(",")
        city_token = ""
        for part in parts:
            cleaned = normalize(part.strip())
            # Skip agency abbreviations (all caps short tokens like DPCC, MPCB)
            if len(cleaned) > 3 and not cleaned.isupper():
                city_token = cleaned
                break

        if city_token:
            station_data = df[df["city_norm"].str.contains(city_token, na=False)]
            print(f"City token '{city_token}' match rows:", len(station_data))

    # =============================
    # 4. FINAL FALLBACK — return empty result rather than
    #    wrong data from entire dataset
    # =============================
    if station_data.empty:
        print("⚠️ No matching data found.")
        return {
            "aqi": None, "pm25": None, "pm10": None,
            "no2": None, "so2": None, "co": None, "ozone": None,
            "temp": None, "rh": None, "ws": None,
            "city": None, "state": None
        }

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

    aqi  = get_latest(station_data["aqi"])
    pm25 = get_latest(station_data["pm2.5"])
    pm10 = get_latest(station_data["pm10"])
    city  = get_latest(station_data["city"])
    state = get_latest(station_data["state"])

    def safe_col(col):
        return get_latest(station_data[col]) if col in station_data.columns else None

    # =============================
    # TEMPERATURE — use lookup table
    # ✅ FIX: Read from station_temp_lookup.csv (validated, deduplicated,
    #         latest per station). Never use raw df rows for temp.
    # =============================
    temp = TEMP_LOOKUP.get(station_name.strip(), None)

    # If exact key not found, try a case-insensitive search
    if temp is None:
        station_lower = station_name.strip().lower()
        for key, val in TEMP_LOOKUP.items():
            if key.lower() == station_lower:
                temp = val
                break

    result = {
        "aqi":   round(float(aqi),  1) if aqi   is not None else None,
        "pm25":  round(float(pm25), 1) if pm25  is not None else None,
        "pm10":  round(float(pm10), 1) if pm10  is not None else None,

        "no2":   safe_col("NO2"),
        "so2":   safe_col("SO2"),
        "co":    safe_col("CO"),
        "ozone": safe_col("OZONE"),

        # ✅ temp comes from lookup, NOT from raw df rows
        "temp": temp,
        "rh":   safe_col("RH"),
        "ws":   safe_col("WS"),

        "city":  city,
        "state": state
    }

    print("✅ FINAL OUTPUT:", result)
    return result