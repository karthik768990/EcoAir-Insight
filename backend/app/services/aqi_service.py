import pandas as pd
import os

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

# 🔥 Clean station names
df["station"] = df["station"].astype(str).str.strip().str.lower()


def get_current_aqi(station_name: str):
    """
    Returns latest AQI + pollutant data for a station
    """

    station_name = station_name.strip().lower()

    station_data = df[df["station"] == station_name]

    if station_data.empty:
        return {
            "aqi": None,
            "pm25": None,
            "pm10": None,
            "pollutant": None,
            "city": None,
            "state": None
        }

    # Sort by latest date
    station_data = station_data.sort_values("date")

    # Drop invalid rows
    station_data = station_data.dropna(subset=["aqi", "pm2.5", "pm10"])

    if station_data.empty:
        return {
            "aqi": None,
            "pm25": None,
            "pm10": None,
            "pollutant": None,
            "city": None,
            "state": None
        }

    latest = station_data.iloc[-1]

    return {
        "aqi": float(latest["aqi"]),
        "pm25": float(latest["pm2.5"]),
        "pm10": float(latest["pm10"]),
        "pollutant": latest.get("pollutant", "Unknown"),
        "city": latest.get("city", ""),
        "state": latest.get("state", "")
    }