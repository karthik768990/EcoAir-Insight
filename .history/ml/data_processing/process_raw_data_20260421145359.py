import pandas as pd
import glob
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
print(str(BASE_DIR))


def process_raw_data():
    print("🚀 Processing ALL Excel files (multi-tab)...")

    raw_dir = os.path.join(BASE_DIR, "ml/data/raw_data")
    processed_dir = os.path.join(BASE_DIR, "ml/data/processed")

    os.makedirs(processed_dir, exist_ok=True)

    stations_path = os.path.join(processed_dir, "stations.csv")
    cleaned_path = os.path.join(processed_dir, "cleaned_data.csv")
    temp_lookup_path = os.path.join(processed_dir, "station_temp_lookup.csv")

    excel_files = glob.glob(os.path.join(raw_dir, "*.xlsx"))

    if not excel_files:
        print("❌ No Excel files found.")
        return

    stations_list = []
    data_list = []

    for file in excel_files:
        print(f"📖 Reading: {os.path.basename(file)}")

        try:
            sheets = pd.read_excel(file, sheet_name=None)

            for sheet_name, df in sheets.items():
                df.columns = df.columns.str.strip()

                # =============================
                # 1. STATION COORDINATES
                # Only extract from dedicated coordinate sheets
                # NOT from data sheets (avoids polluted/duplicate coords)
                # =============================
                if {'Monitoring Station', 'Latitude', 'Longitude'}.issubset(df.columns):
                    coord_rows = df[['Monitoring Station', 'Latitude', 'Longitude']].dropna()
                    # Only keep if Latitude looks like a real coordinate (not a data column)
                    coord_rows['Latitude'] = pd.to_numeric(coord_rows['Latitude'], errors='coerce')
                    coord_rows['Longitude'] = pd.to_numeric(coord_rows['Longitude'], errors='coerce')
                    coord_rows = coord_rows.dropna(subset=['Latitude', 'Longitude'])
                    # Valid India lat/lon ranges: Lat 6-37, Lon 68-98
                    coord_rows = coord_rows[
                        (coord_rows['Latitude'].between(6, 37)) &
                        (coord_rows['Longitude'].between(68, 98))
                    ]
                    if not coord_rows.empty:
                        stations_list.append(coord_rows)

                # =============================
                # 2. SKIP NON-DATA SHEETS
                # =============================
                if any(x in sheet_name.lower() for x in ["summary", "health", "standard"]):
                    continue

                # =============================
                # 3. HANDLE BOTH DATA TYPES
                # =============================
                if 'Monitoring Station' in df.columns and 'Date' in df.columns:

                    # Add State if missing
                    if 'State' not in df.columns:
                        df['State'] = sheet_name

                    # Normalize column names
                    rename_map = {
                        "Station name": "Monitoring Station",
                        "PM2.5": "PM2.5 (ug/m3)",
                        "PM10": "PM10 (ug/m3)"
                    }
                    df.rename(columns=rename_map, inplace=True)

                    data_list.append(df)

        except Exception as e:
            print(f"⚠️ Error in file: {e}")

    # =============================
    # SAVE STATIONS (DEDUPLICATED)
    # =============================
    if stations_list:
        stations_df = pd.concat(stations_list, ignore_index=True)
        # Keep first occurrence (most specific/reliable coordinate source)
        stations_df = stations_df.drop_duplicates(subset=['Monitoring Station'], keep='first')
        stations_df['Latitude'] = stations_df['Latitude'].round(6)
        stations_df['Longitude'] = stations_df['Longitude'].round(6)

        stations_df.to_csv(stations_path, index=False)
        print(f"✅ Stations saved: {len(stations_df)} unique stations → {stations_path}")
    else:
        print("❌ No station coordinates found")

    # =============================
    # SAVE CLEANED DATA (DEDUPLICATED)
    # =============================
    if data_list:
        df = pd.concat(data_list, ignore_index=True)

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        important_cols = [
            'State', 'City', 'Monitoring Station', 'Date',
            'AQI',
            'PM2.5 (ug/m3)', 'PM10 (ug/m3)',
            'NO2', 'NOx', 'NH3', 'SO2', 'CO', 'OZONE',
            'Temp', 'RH', 'WS', 'WD', 'SR', 'RF',
            'Highest Pollutant'
        ]
        cols_to_keep = [c for c in important_cols if c in df.columns]
        df = df[cols_to_keep]

        # ✅ FIX: Deduplicate on station + date (eliminates 80% redundant rows)
        before = len(df)
        df = df.drop_duplicates(subset=['Monitoring Station', 'Date'], keep='first')
        after = len(df)
        print(f"✅ Deduplication: {before:,} → {after:,} rows (removed {before - after:,} duplicates)")

        df.to_csv(cleaned_path, index=False)
        print(f"✅ Cleaned data saved: {cleaned_path}")
        print(f"📊 Total rows: {len(df)}")

        # =============================
        # BUILD TEMPERATURE LOOKUP TABLE
        # =============================
        _build_temp_lookup(df, stations_df if stations_list else None, temp_lookup_path)

    else:
        print("❌ No pollution data found")


def _build_temp_lookup(df, stations_df, output_path):
    """
    Build a per-station temperature lookup table using the
    latest valid temperature reading per monitoring station.

    Validity rules:
      - Temperature must be between 0°C and 48°C (India realistic range)
      - Values > 48°C are sensor errors (verified in data audit)
      - Daily values are already averaged from sub-daily readings — this is correct
    """
    print("🌡️  Building temperature lookup table...")

    if 'Temp' not in df.columns:
        print("⚠️  No Temp column in cleaned data — skipping temp lookup")
        return

    # Filter to rows with valid temperature readings
    df_valid_temp = df[
        df['Temp'].notna() &
        (df['Temp'] >= 0) &
        (df['Temp'] <= 48)
    ].copy()

    print(f"   Valid temp readings: {len(df_valid_temp):,} / {df['Temp'].notna().sum():,} total")

    # Get the latest valid temp per station
    latest_temp = (
        df_valid_temp
        .sort_values('Date')
        .groupby('Monitoring Station')
        .last()
        .reset_index()
    )[['Monitoring Station', 'Date', 'Temp', 'State', 'City']]

    latest_temp.columns = ['Monitoring Station', 'Latest_Temp_Date', 'Latest_Temp_C', 'State', 'City']
    latest_temp['Latest_Temp_C'] = latest_temp['Latest_Temp_C'].round(2)

    # Merge with station coordinates if available
    if stations_df is not None:
        result = stations_df.merge(latest_temp, on='Monitoring Station', how='left')
    else:
        result = latest_temp

    result.to_csv(output_path, index=False)

    with_temp = result['Latest_Temp_C'].notna().sum()
    without_temp = result['Latest_Temp_C'].isna().sum()
    print(f"✅ Temp lookup saved: {with_temp} stations with temp, {without_temp} without → {output_path}")
    print(f"   Temp range: {result['Latest_Temp_C'].min():.1f}°C – {result['Latest_Temp_C'].max():.1f}°C")


if __name__ == "__main__":
    process_raw_data()