import pandas as pd
import glob
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)


def process_raw_data():
    print("Starting Pan-India data extraction (Reading ALL tabs)...")

    raw_dir = os.path.join(BASE_DIR, "ml/data/raw_data")
    processed_dir = os.path.join(BASE_DIR, "ml/data/processed")
    os.makedirs(processed_dir, exist_ok=True)

    all_excel_files = glob.glob(os.path.join(raw_dir, '*.xlsx'))

    if not all_excel_files:
        print("❌ ERROR: No XLSX files found.")
        return

    stations_list = []
    aqi_data_list = []

    for file in all_excel_files:
        print(f"📖 Opening Workbook: {os.path.basename(file)}...")
        try:
            all_sheets = pd.read_excel(file, sheet_name=None)

            for sheet_name, df in all_sheets.items():
                df.columns = df.columns.str.strip()

                # 1. Look for Coordinates — validate they are real lat/lon values
                if 'Monitoring Station' in df.columns and 'Latitude' in df.columns and 'Longitude' in df.columns:
                    temp_stations = df[['Monitoring Station', 'Latitude', 'Longitude']].copy()
                    temp_stations['Latitude'] = pd.to_numeric(temp_stations['Latitude'], errors='coerce')
                    temp_stations['Longitude'] = pd.to_numeric(temp_stations['Longitude'], errors='coerce')
                    temp_stations = temp_stations.dropna()
                    # Valid India lat/lon ranges
                    temp_stations = temp_stations[
                        temp_stations['Latitude'].between(6, 37) &
                        temp_stations['Longitude'].between(68, 98)
                    ]
                    if not temp_stations.empty:
                        stations_list.append(temp_stations)

                # 2. Skip non-data sheets
                if 'Summary' in sheet_name or 'Health' in sheet_name or 'Standards' in sheet_name:
                    continue

                # 3. Look for Pollution Data
                if 'Monitoring Station' in df.columns and 'Date' in df.columns and 'AQI' in df.columns:
                    if 'State' not in df.columns:
                        df['State'] = sheet_name
                    aqi_data_list.append(df)

        except Exception as e:
            print(f"⚠️ Skipped a corrupted file or tab: {e}")

    # --- SAVE STATIONS ---
    if stations_list:
        stations_df = pd.concat(stations_list, ignore_index=True).drop_duplicates(subset=['Monitoring Station'])
        stations_df.to_csv(os.path.join(processed_dir, 'stations.csv'), index=False)
        print(f"✅ Success: Mapped {len(stations_df)} unique stations across India.")
    else:
        print("❌ ERROR: No coordinates found in any tabs.")
        return

    # --- SAVE AQI + TEMP DATA ---
    if aqi_data_list:
        combined_df = pd.concat(aqi_data_list, ignore_index=True)
        combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
        combined_df = combined_df.dropna(subset=['Date', 'AQI'])

        # ✅ Include Temp in target columns (was missing in original clean_data.py)
        target_cols = [
            'State', 'City', 'Monitoring Station', 'Date',
            'AQI', 'PM2.5 (ug/m3)', 'PM10 (ug/m3)',
            'Temp',                      # ← ADDED
            'WD',                        # ← ADDED
            'Highest Pollutant'
        ]
        cols_to_keep = [c for c in target_cols if c in combined_df.columns]
        cleaned_df = combined_df[cols_to_keep]

        # ✅ FIX: Deduplicate — same station+date from multiple Excel files
        before = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates(subset=['Monitoring Station', 'Date'], keep='first')
        after = len(cleaned_df)
        print(f"✅ Deduplication: {before:,} → {after:,} rows (removed {before - after:,} duplicates)")

        cleaned_df.to_csv(os.path.join(processed_dir, 'cleaned_data.csv'), index=False)
        print(f"✅ Success: Consolidated {len(cleaned_df)} historical records from ALL tabs.")
    else:
        print("❌ ERROR: No historical AQI data found.")


if __name__ == "__main__":
    process_raw_data()