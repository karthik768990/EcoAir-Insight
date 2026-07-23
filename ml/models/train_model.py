import pandas as pd
import numpy as np
import os
import sys
import warnings
from sklearn.ensemble import HistGradientBoostingRegressor
from joblib import Parallel, delayed
from tqdm import tqdm

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.app.database import engine
from backend.app.models import Station, Prediction
from sqlalchemy.orm import sessionmaker

# =============================
# Feature Engineering
# =============================
def create_features(group):
    group = group.sort_values("YearMonth").copy()
    group["Month_Index"] = np.arange(len(group))
    group["Month"] = group["YearMonth"].dt.month
    group["sin_month"] = np.sin(2 * np.pi * group["Month"] / 12)
    group["cos_month"] = np.cos(2 * np.pi * group["Month"] / 12)
    group["lag_1"] = group["AQI"].shift(1)
    group["lag_2"] = group["AQI"].shift(2)
    group["lag_3"] = group["AQI"].shift(3)
    group["rolling_mean_3"] = group["AQI"].rolling(3).mean()
    group["rolling_std_3"] = group["AQI"].rolling(3).std()
    group = group.dropna()
    return group

# =============================
# Train per station
# =============================
def train_station(station, group):
    try:
        group = create_features(group)
        if len(group) < 24:
            return []

        features = ["Month_Index", "sin_month", "cos_month", "lag_1", "lag_2", "lag_3", "rolling_mean_3", "rolling_std_3"]
        X = group[features]
        y = group["AQI"]

        model = HistGradientBoostingRegressor(max_depth=6, learning_rate=0.05, max_iter=200, random_state=42)
        model.fit(X, y)

        future_preds = []
        last_row = group.iloc[-1:].copy()

        for i in range(60):  # 5 years
            next_row = last_row.copy()
            next_row["Month_Index"] = next_row["Month_Index"].values[0] + 1
            current_month = int(next_row["Month"].values[0])
            next_month = (current_month % 12) + 1
            next_row["Month"] = next_month
            next_row["sin_month"] = np.sin(2 * np.pi * next_month / 12)
            next_row["cos_month"] = np.cos(2 * np.pi * next_month / 12)

            lag1 = last_row["AQI"].values[0]
            lag2 = next_row["lag_1"].values[0]
            lag3 = next_row["lag_2"].values[0]
            next_row["lag_1"] = lag1
            next_row["lag_2"] = lag2
            next_row["lag_3"] = lag3

            recent_values = [lag1, lag2, lag3]
            next_row["rolling_mean_3"] = np.mean(recent_values)
            next_row["rolling_std_3"] = np.std(recent_values)

            pred = model.predict(next_row[features])[0]
            pred = max(0, pred)
            future_preds.append(pred)

            next_row["AQI"] = pred
            last_row = next_row.copy()

        std_dev = np.std(future_preds)
        results = []
        for i, val in enumerate(future_preds):
            results.append({
                "Monitoring Station": station,
                "Month_Ahead": i + 1,
                "Predicted_AQI": round(val, 2),
                "Lower_Bound": round(max(0, val - std_dev), 2),
                "Upper_Bound": round(val + std_dev, 2)
            })
        return results

    except Exception as e:
        print(f"Error in station {station}: {e}")
        return []

def normalize(text):
    import re
    if pd.isna(text):
        return ""
    text = str(text).lower().strip()
    return re.sub(r"[^a-z0-9 ]", "", text)

# =============================
# MAIN PIPELINE
# =============================
def train_and_predict():
    print("Starting ML pipeline...")

    data_path = os.path.join(BASE_DIR, "data", "processed", "cleaned_data.csv")
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}!")
        return

    print("Loading dataset...")
    df = pd.read_csv(data_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "AQI", "Monitoring Station"])

    df["YearMonth"] = df["Date"].dt.to_period("M")
    df = df.groupby(["Monitoring Station", "YearMonth"])["AQI"].mean().reset_index()
    df["YearMonth"] = df["YearMonth"].dt.to_timestamp()

    print("Training models in parallel...")
    grouped = list(df.groupby("Monitoring Station"))
    results = Parallel(n_jobs=-1, backend="loky")(
        delayed(train_station)(station, group) for station, group in tqdm(grouped)
    )

    predictions = [item for sublist in results for item in sublist]
    pred_df = pd.DataFrame(predictions)
    
    # Save to CSV for backup
    output_path = os.path.join(BASE_DIR, "data", "processed", "predictions_5yr_advanced.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pred_df.to_csv(output_path, index=False)
    
    print(f"Completed for {len(pred_df) // 60} stations")
    
    # Save to Database idempotently
    print("Saving predictions to the database...")
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        stations = {s.name_norm: s.id for s in session.query(Station).all()}
        
        # Clear old predictions
        session.query(Prediction).delete()
        
        batch = []
        for _, row in pred_df.iterrows():
            station_name = row["Monitoring Station"]
            norm_name = normalize(station_name)
            station_id = stations.get(norm_name)
            
            if not station_id:
                continue
                
            pred = Prediction(
                station_id=station_id,
                month_ahead=row["Month_Ahead"],
                predicted_aqi=row["Predicted_AQI"],
                lower_bound=row.get("Lower_Bound"),
                upper_bound=row.get("Upper_Bound")
            )
            batch.append(pred)
        
        session.bulk_save_objects(batch)
        session.commit()
        print("Successfully saved predictions to database.")
    except Exception as e:
        session.rollback()
        print(f"Error saving to database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    train_and_predict()