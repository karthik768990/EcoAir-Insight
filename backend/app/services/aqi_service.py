import pandas as pd
import os
import re

# 🔥 Resolve file path
current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/cleaned_data.csv")
)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"AQI file not found at: {data_path}")

# 🔥 Load dataset once
df = pd.read_csv(data_path)

# 🔥 Normalize column names
df.columns = df.columns.str.strip()

# 🔥 Rename to clean internal schema
df.rename(columns={
    "Monitoring Station": "station",
    "State": "state",
    "City": "city",
    "Date": "date",
    "AQI": "aqi",
    "PM2.5 (ug/m3)": "pm2.5",
    "PM10 (ug/m3)": "pm10",
    "Highest Pollutant": "pollutant"
}, inplace=True)

# 🔥 Convert date
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 🔥 Clean station names (basic)
df["station"] = df["station"].astype(str).str.strip().str.lower()


# 🔥 ADVANCED NORMALIZATION FUNCTION
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9 ]", "", text)  # remove symbols like , -
    return text


# 🔥 Create normalized column ONCE
df["station_norm"] = df["station"].apply(normalize)


def get_current_aqi(station_name: str):
    """
    Returns latest AQI + pollutant data for a station
    (with fallback to city-level data)
    """

    print("\n🔥 FUNCTION CALLED")
    print("Incoming station:", station_name)

    station_name = station_name.strip().lower()

    # 🔥 Try exact match
    station_data = df[df["station"] == station_name]

    # 🔥 IF NOT FOUND → FALLBACK
    if station_data.empty:
        print("⚠️ Exact station not found. Trying fallback...")

        # Try matching by city name
        words = station_name.split()

        # Try each word (to catch "chennai", "delhi", etc.)
        city_match = pd.DataFrame()

        for word in words:
            temp = df[df["city"].str.lower().str.contains(word, na=False)]
            if not temp.empty:
                city_match = temp
                print(f"✅ Found fallback using word: {word}")
                break

        # If still empty → take ANY data (last fallback)
        if city_match.empty:
            print("⚠️ No city match. Using global fallback.")
            station_data = df
        else:
            station_data = city_match

    # 🔥 Sort latest
    station_data = station_data.sort_values("date", ascending=False)

    # 🔥 Extract latest valid values
    def get_latest_valid(series):
        series = series.dropna()
        return series.iloc[0] if not series.empty else None

    aqi = get_latest_valid(station_data["aqi"])
    pm25 = get_latest_valid(station_data["pm2.5"])
    pm10 = get_latest_valid(station_data["pm10"])
    pollutant = get_latest_valid(station_data["pollutant"])
    city = get_latest_valid(station_data["city"])
    state = get_latest_valid(station_data["state"])

    print("✅ FINAL VALUES:", aqi, pm25, pm10)
         
    return {
        "aqi": float(aqi) if aqi is not None else None,
        "pm25": float(pm25) if pm25 is not None else None,
        "pm10": float(pm10) if pm10 is not None else None,
        "pollutant": pollutant if pollutant is not None else "Unknown",
        "city": city if city is not None else "",
        "state": state if state is not None else ""
    }