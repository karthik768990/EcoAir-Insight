import pandas as pd
import os


def fix_predictions():
    print("🔧 Removing duplicate cycles and reducing to 12 months...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    processed_dir = os.path.abspath(os.path.join(current_dir, "..", "data", "processed"))

    input_path = os.path.join(processed_dir, "predictions_5yr_advanced.csv")

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return

    df = pd.read_csv(input_path)

    # Create 12-month cycle
    df["Month"] = ((df["Month_Ahead"] - 1) % 12) + 1

    # 🔥 Keep ONLY 12 rows per station (median aggregation)
    final_df = df.groupby(["Monitoring Station", "Month"]).agg({
        "Predicted_AQI": "median",
        "Lower_Bound": "median",
        "Upper_Bound": "median"
    }).reset_index()

    # Sort properly
    final_df = final_df.sort_values(["Monitoring Station", "Month"])

    # Save file
    output_path = os.path.join(processed_dir, "predictions_1yr_cleaned.csv")
    final_df.to_csv(output_path, index=False)

    print("✅ Successfully reduced predictions!")
    print(f"📉 Rows reduced from {len(df)} → {len(final_df)}")
    print(f"📁 Saved to: {output_path}")


if __name__ == "__main__":
    fix_predictions()