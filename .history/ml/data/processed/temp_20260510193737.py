import pandas as pd
import os

# =========================
# CONFIGURATION
# =========================

INPUT_FILE = "cleaned_data.csv"
OUTPUT_FILE = "new_cleaned_data.csv"

# Column name
LABEL_COLUMN = "monitoring station"

# Maximum rows to keep per label
MAX_ROWS_PER_LABEL = 5500


# =========================
# LOAD DATA
# =========================

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original rows: {len(df)}")


# =========================
# OPTIONAL DATE SORT
# =========================

if "Date" in df.columns:
    print("Sorting by latest dates...")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df = df.sort_values("Date", ascending=False)


# =========================
# REDUCE DATASET
# =========================

print("Reducing repeated rows per label...")

reduced_df = (
    df.groupby(LABEL_COLUMN, group_keys=False)
      .head(MAX_ROWS_PER_LABEL)
)

print(f"Reduced rows: {len(reduced_df)}")


# =========================
# SAVE FILE
# =========================

reduced_df.to_csv(OUTPUT_FILE, index=False)

# File size check
size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)

print(f"Output size: {size_mb:.2f} MB")
print(f"Saved to: {OUTPUT_FILE}")

