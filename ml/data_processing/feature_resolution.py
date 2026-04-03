import pandas as pd
import os


def fix_predictions():
    print("🔧 Fixing prediction duplication issue...")

    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to processed folder
    processed_dir = os.path.join(current_dir, "..", "data", "processed")
    processed_dir = os.path.abspath(processed_dir)

    input_path = os.path.join(processed_dir, "predictions_5yr_advanced.csv")

    if not os.path.exists(input_path):
        print(f"❌ Prediction file not found at: {input_path}")
        return

    print("📥 Loading predictions...")
    df = pd.read_csv(input_path)

    # Create cycle grouping (1–12 repeated)
    df["Month_Cycle"] = ((df["Month_Ahead"] - 1) % 12) + 1

    # Aggregate using median (robust)
    agg_df = df.groupby(["Monitoring Station", "Month_Cycle"]).agg({
        "Predicted_AQI": "median",
        "Lower_Bound": "median",
        "Upper_Bound": "median"
    }).reset_index()

    # Rename for clarity
    agg_df.rename(columns={"Month_Cycle": "Month"}, inplace=True)

    # Expand back to 60 months (cleaned)
    final_rows = []

    for station, group in agg_df.groupby("Monitoring Station"):
        for i in range(60):
            month = (i % 12) + 1
            row = group[group["Month"] == month].iloc[0]

            final_rows.append({
                "Monitoring Station": station,
                "Month_Ahead": i + 1,
                "Predicted_AQI": row["Predicted_AQI"],
                "Lower_Bound": row["Lower_Bound"],
                "Upper_Bound": row["Upper_Bound"]
            })

    final_df = pd.DataFrame(final_rows)

    # Save in SAME processed folder
    output_path = os.path.join(processed_dir, "predictions_5yr_cleaned.csv")
    final_df.to_csv(output_path, index=False)

    print("✅ Fix completed!")
    print(f"📁 Saved to: {output_path}")


if __name__ == "__main__":
    fix_predictions()