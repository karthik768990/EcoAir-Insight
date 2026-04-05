import pandas as pd
import os

# 🔥 Resolve path
current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.abspath(
    os.path.join(current_dir, "../../../ml/data/processed/predictions_5yr_advanced.csv")
)

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Prediction file not found at: {data_path}")

# 🔥 Load once
df = pd.read_csv(data_path)

# 🔥 Normalize columns
df.columns = df.columns.str.strip()

# 🔥 Rename to clean schema
df.rename(columns={
    "Monitoring Station": "station",
    "Month_Ahead": "month",
    "Predicted_AQI": "aqi",
    "Lower_Bound": "lower",
    "Upper_Bound": "upper"
}, inplace=True)

# 🔥 Clean station names
df["station"] = df["station"].astype(str).str.strip().str.lower()


def get_prediction(station_name: str):
    """
    Returns AQI prediction with bounds
    """

    station_name = station_name.strip().lower()

    # 🔥 Flexible matching (VERY IMPORTANT)
    station_data = df[df["station"].str.contains(station_name, na=False)]

    if station_data.empty:
        return []

    # ✅ Correct column
    station_data = station_data.sort_values(by="month")

    return [
        {
            "month": int(row["month"]),
            "aqi": float(row["aqi"]),
            "lower": float(row["lower"]),
            "upper": float(row["upper"])
        }
        for _, row in station_data.iterrows()
    ]