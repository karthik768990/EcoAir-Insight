import pandas as pd
import numpy as np
import os
import warnings
from sklearn.ensemble import HistGradientBoostingRegressor
from joblib import Parallel, delayed
from tqdm import tqdm

warnings.filterwarnings("ignore")


# =============================
# Feature Engineering
# =============================
def create_features(group):
    group = group.sort_values("YearMonth").copy()

    group["Month_Index"] = np.arange(len(group))
    group["Month"] = group["YearMonth"].dt.month

    # Seasonality
    group["sin_month"] = np.sin(2 * np.pi * group["Month"] / 12)
    group["cos_month"] = np.cos(2 * np.pi * group["Month"] / 12)

    # Lag features
    group["lag_1"] = group["AQI"].shift(1)
    group["lag_2"] = group["AQI"].shift(2)
    group["lag_3"] = group["AQI"].shift(3)

    # Rolling features
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

        features = [
            "Month_Index", "sin_month", "cos_month",
            "lag_1", "lag_2", "lag_3",
            "rolling_mean_3", "rolling_std_3"
        ]

        X = group[features]
        y = group["AQI"]

        model = HistGradientBoostingRegressor(
            max_depth=6,
            learning_rate=0.05,
            max_iter=200,
            random_state=42
        )

        model.fit(X, y)

        # =============================
        # Future prediction (recursive)
        # =============================
        future_preds = []
        last_row = group.iloc[-1:].copy()

        for i in range(60):  # 5 years
            next_row = last_row.copy()

            # Update time index
            next_row["Month_Index"] = next_row["Month_Index"].values[0] + 1

            # Update month
            current_month = int(next_row["Month"].values[0])
            next_month = (current_month % 12) + 1
            next_row["Month"] = next_month

            # Seasonality
            next_row["sin_month"] = np.sin(2 * np.pi * next_month / 12)
            next_row["cos_month"] = np.cos(2 * np.pi * next_month / 12)

            # Lag updates
            lag1 = last_row["AQI"].values[0]
            lag2 = next_row["lag_1"].values[0]
            lag3 = next_row["lag_2"].values[0]

            next_row["lag_1"] = lag1
            next_row["lag_2"] = lag2
            next_row["lag_3"] = lag3

            # Rolling stats
            recent_values = [lag1, lag2, lag3]
            next_row["rolling_mean_3"] = np.mean(recent_values)
            next_row["rolling_std_3"] = np.std(recent_values)

            # Prediction
            pred = model.predict(next_row[features])[0]
            pred = max(0, pred)

            future_preds.append(pred)

            # Update for next iteration
            next_row["AQI"] = pred
            last_row = next_row.copy()

        # Confidence interval
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
        print(f"⚠️ Error in station {station}: {e}")
        return []


# =============================
# MAIN PIPELINE
# =============================
def train_and_predict():
    print("🚀 Industry-level ML pipeline started...")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "cleaned_data", "cleaned_data.csv")

    if not os.path.exists(data_path):
        print("❌ Data not found!")
        return

    print("📥 Loading dataset...")
    df = pd.read_csv(data_path)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "AQI", "Monitoring Station"])

    # Monthly aggregation (IMPORTANT for performance)
    df["YearMonth"] = df["Date"].dt.to_period("M")
    df = df.groupby(["Monitoring Station", "YearMonth"])["AQI"].mean().reset_index()
    df["YearMonth"] = df["YearMonth"].dt.to_timestamp()

    print("⚙️ Training models in parallel...")

    grouped = list(df.groupby("Monitoring Station"))

    results = Parallel(n_jobs=-1, backend="loky")(
        delayed(train_station)(station, group)
        for station, group in tqdm(grouped)
    )

    predictions = [item for sublist in results for item in sublist]

    pred_df = pd.DataFrame(predictions)

    output_path = os.path.join(base_dir, "data", "processed", "predictions_5yr_advanced.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pred_df.to_csv(output_path, index=False)

    print(f"✅ Completed for {len(pred_df) // 60} stations")
    print(f"📁 Saved to: {output_path}")


if __name__ == "__main__":
    train_and_predict()