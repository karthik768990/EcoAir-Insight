import pandas as pd
import os

INPUT_FILE = "cleaned_data.csv"
OUTPUT_FILE = "cleaned_data_deploy.csv"

LABEL_COLUMN = "monitoring station"

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original rows:", len(df))

# Convert dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Sort latest first
df = df.sort_values("Date", ascending=False)

# Keep ONLY latest row per station
reduced_df = (
    df.groupby(LABEL_COLUMN, as_index=False)
      .first()
)

print("Reduced rows:", len(reduced_df))

reduced_df.to_csv(OUTPUT_FILE, index=False)

size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)

print(f"Output size: {size_mb:.2f} MB")
