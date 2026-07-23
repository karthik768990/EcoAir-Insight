import pandas as pd
import glob
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
print(BASE_DIR)
def process_raw_data():
    print("Processing ALL Excel files (multi-tab)...")

    raw_dir = os.path.join(BASE_DIR, "ml/data/raw_data")
    processed_dir = os.path.join(BASE_DIR, "ml/data/processed")

    os.makedirs(processed_dir, exist_ok=True)

    stations_path = os.path.join(processed_dir, "stations.csv")
    cleaned_path = os.path.join(processed_dir, "cleaned_data.csv")

    excel_files = [
    f for f in glob.glob(os.path.join(raw_dir, "*.xlsx"))
    if not os.path.basename(f).startswith("~$")
]

    if not excel_files:
        print("No Excel files found.")
        return

    stations_list = []
    data_list = []

    for file in excel_files:
        print(f"Reading: {os.path.basename(file)}")

        try:
            sheets = pd.read_excel(file, sheet_name=None)

            for sheet_name, df in sheets.items():
                # Normalize column names
                df.columns = df.columns.map(lambda x: str(x).strip().lower())

                # =============================
                # 1. STATION COORDINATES
                # =============================
                if {'monitoring station', 'latitude', 'longitude'}.issubset(df.columns):
                    stations_list.append(
                        df[['monitoring station', 'latitude', 'longitude']].dropna()
                    )

                # =============================
                # 2. SKIP NON-DATA SHEETS
                # =============================
                if any(x in sheet_name.lower() for x in ["summary", "health", "standard"]):
                    continue

                # =============================
                # 3. VALID DATA CHECK
                # =============================
                if 'monitoring station' in df.columns and 'date' in df.columns:

                    # Add state if missing
                    if 'state' not in df.columns:
                        df['state'] = sheet_name

                    # =============================
                    # NORMALIZE COLUMN NAMES
                    # =============================
                    rename_map = {
                        'pm2.5 (ug/m3)': 'pm2.5',
                        'pm10 (ug/m3)': 'pm10',
                        'no2 (ug/m3)': 'no2',
                        'no2': 'no2',
                        'so2 (ug/m3)': 'so2',
                        'so2': 'so2',
                        'co (mg/m3)': 'co',
                        'co': 'co',
                        'ozone (ug/m3)': 'ozone',
                        'o3': 'ozone',
                        'temp': 'temp',
                        'rh': 'rh',
                        'ws': 'ws',
                        'monitoring station': 'monitoring station',
                        'city': 'city',
                        'state': 'state',
                        'aqi': 'aqi',
                        'date': 'date'
                    }

                    df.rename(columns=rename_map, inplace=True)
                    data_list.append(df)

        except Exception as e:
            print(f"Error in file: {e}")

    # =============================
    # SAVE STATIONS
    # =============================
    if stations_list:
        stations_df = pd.concat(stations_list, ignore_index=True)
        stations_df = stations_df.drop_duplicates(subset=['monitoring station'])

        stations_df.to_csv(stations_path, index=False)
        print(f"Stations saved: {stations_path}")
    else:
        print("No station coordinates found")

    # =============================
    # SAVE CLEANED DATA
    # =============================
    if data_list:
        df = pd.concat(data_list, ignore_index=True)

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date', 'aqi'])

        # FINAL COLUMN SELECTION
        important_base = [
            'state', 'city', 'monitoring station', 'date', 'aqi'
        ]

        pollutant_candidates = [
            'pm2.5', 'pm10', 'no2', 'nox', 'nh3',
            'so2', 'co', 'ozone',
            'temp', 'rh', 'ws'
        ]

        cols_to_keep = important_base + [
            col for col in pollutant_candidates if col in df.columns
        ]

        df = df[cols_to_keep]

        print("FINAL COLUMNS:", df.columns.tolist())
        df.to_csv(cleaned_path, index=False)
        print(f"Cleaned data saved: {cleaned_path}")
        print(f"Total rows: {len(df)}")
    else:
        print("No pollution data found")


if __name__ == "__main__":
    process_raw_data()