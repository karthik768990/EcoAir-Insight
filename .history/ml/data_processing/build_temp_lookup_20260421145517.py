"""
build_temp_lookup.py
--------------------
Generates station_temp_lookup.csv from existing cleaned_data.csv + stations.csv.

Run this ONCE after process_raw_data.py to create the temperature reference table
used by the FastAPI backend.

Output columns:
  Monitoring Station | Latitude | Longitude | State | City | Latest_Temp_Date | Latest_Temp_C

Usage:
  python build_temp_lookup.py
"""

import pandas as pd
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)


def build_temp_lookup():
    processed_dir = os.path.join(BASE_DIR, "ml/data/processed")

    cleaned_path = os.path.join(processed_dir, "cleaned_data.csv")
    stations_path = os.path.join(processed_dir, "stations.csv")
    output_path = os.path.join(processed_dir, "station_temp_lookup.csv")

    if not os.path.exists(cleaned_path):
        print(f"❌ cleaned_data.csv not found at: {cleaned_path}")
        return

    if not os.path.exists(stations_path):
        print(f"❌ stations.csv not found at: {stations_path}")
        return

    print("📥 Loading data...")
    df = pd.read_csv(cleaned_path)
    stations = pd.read_csv(stations_path)

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Ensure lat/lon are numeric
    stations['Latitude'] = pd.to_numeric(stations['Latitude'], errors='coerce')
    stations['Longitude'] = pd.to_numeric(stations['Longitude'], errors='coerce')

    if 'Temp' not in df.columns:
        print("❌ No 'Temp' column found in cleaned_data.csv")
        print("   Re-run process_raw_data.py first — it now retains the Temp column.")
        return

    print(f"📊 Loaded {len(df):,} rows, {df['Temp'].notna().sum():,} with temperature readings")
    print(f"📍 {len(stations)} monitoring stations with coordinates")

    # ── Step 1: Deduplicate ───────────────────────────────────────────
    # Multiple Excel files create duplicate rows for same station+date.
    # Always take the first (most specific source wins).
    before = len(df)
    df = df.drop_duplicates(subset=['Monitoring Station', 'Date'], keep='first')
    print(f"🔁 Deduplication: {before:,} → {len(df):,} rows")

    # ── Step 2: Validate temperature ────────────────────────────────
    # India realistic range: 0°C (winter Himalayan foothills) to 48°C (peak Rajasthan summer)
    # Values > 48°C confirmed as sensor errors from data audit (e.g., Vile Parle 52°C in monsoon)
    df_valid_temp = df[
        df['Temp'].notna() &
        (df['Temp'] >= 0) &
        (df['Temp'] <= 48)
    ].copy()

    removed = df['Temp'].notna().sum() - len(df_valid_temp)
    print(f"🌡️  Temperature validation: removed {removed} sensor-error readings (>48°C or <0°C)")
    print(f"   Valid temp rows: {len(df_valid_temp):,}")

    # ── Step 3: Latest valid temp per station ───────────────────────
    # NOTE: Temperature values like 13.217708 are CORRECT — they are daily averages
    # computed from 15-minute interval sensor readings. This is standard practice.
    # Do NOT round these aggressively; display as XX.X in the UI.
    latest_temp = (
        df_valid_temp
        .sort_values('Date')
        .groupby('Monitoring Station')
        .last()
        .reset_index()
    )

    # Keep only the columns we need
    keep_cols = ['Monitoring Station', 'Date', 'Temp']
    if 'State' in latest_temp.columns:
        keep_cols.append('State')
    if 'City' in latest_temp.columns:
        keep_cols.append('City')

    latest_temp = latest_temp[keep_cols]
    col_rename = {'Date': 'Latest_Temp_Date', 'Temp': 'Latest_Temp_C'}
    latest_temp.rename(columns=col_rename, inplace=True)

    # Round to 2 decimal places for clean display
    latest_temp['Latest_Temp_C'] = latest_temp['Latest_Temp_C'].round(2)

    # ── Step 4: Merge with station coordinates ───────────────────────
    result = stations.merge(latest_temp, on='Monitoring Station', how='left')

    # Reorder columns cleanly
    ordered_cols = ['Monitoring Station', 'Latitude', 'Longitude']
    if 'State' in result.columns:
        ordered_cols.append('State')
    if 'City' in result.columns:
        ordered_cols.append('City')
    ordered_cols += ['Latest_Temp_Date', 'Latest_Temp_C']
    result = result[[c for c in ordered_cols if c in result.columns]]

    # ── Step 5: Save ────────────────────────────────────────────────
    result.to_csv(output_path, index=False)

    with_temp = result['Latest_Temp_C'].notna().sum()
    without_temp = result['Latest_Temp_C'].isna().sum()

    print()
    print("✅ station_temp_lookup.csv saved!")
    print(f"   📍 Total stations: {len(result)}")
    print(f"   🌡️  With temperature data: {with_temp}")
    print(f"   ❌ Without temperature (will show N/A in UI): {without_temp}")
    print(f"   🌡️  Temp range: {result['Latest_Temp_C'].min():.1f}°C – {result['Latest_Temp_C'].max():.1f}°C")
    print(f"   📁 Saved to: {output_path}")
    print()
    print("📌 Next step: Update your FastAPI backend to load this file")
    print("   and use Latest_Temp_C for the temperature field.")


if __name__ == "__main__":
    build_temp_lookup()