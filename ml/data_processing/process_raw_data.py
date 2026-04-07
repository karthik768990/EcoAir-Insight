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
                # =============================
                if {'Monitoring Station', 'Latitude', 'Longitude'}.issubset(df.columns):
                    stations_list.append(
                        df[['Monitoring Station', 'Latitude', 'Longitude']].dropna()
                    )

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

                    # Normalize column names (NEW DATA SUPPORT)
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
    # SAVE STATIONS (OVERWRITE)
    # =============================
    if stations_list:
        stations_df = pd.concat(stations_list, ignore_index=True)
        stations_df = stations_df.drop_duplicates(subset=['Monitoring Station'])

        stations_df.to_csv(stations_path, index=False)
        print(f"✅ Stations saved: {stations_path}")
    else:
        print("❌ No station coordinates found")

    # =============================
    # SAVE CLEANED DATA (OVERWRITE)
    # =============================
    if data_list:
        df = pd.concat(data_list, ignore_index=True)

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        important_cols = [
            'State', 'City', 'Monitoring Station', 'Date',

            # AQI core
            'AQI',
            'PM2.5 (ug/m3)', 'PM10 (ug/m3)',

            # NEW pollutants
            'NO2', 'NOx', 'NH3', 'SO2', 'CO', 'OZONE',

            # Weather
            'Temp', 'RH', 'WS', 'WD', 'SR', 'RF',

            'Highest Pollutant'
        ]

        cols_to_keep = [c for c in important_cols if c in df.columns]

        df = df[cols_to_keep]

        df.to_csv(cleaned_path, index=False)

        print(f"✅ Cleaned data saved: {cleaned_path}")
        print(f"📊 Total rows: {len(df)}")

    else:
        print("❌ No pollution data found")


if __name__ == "__main__":
    process_raw_data()