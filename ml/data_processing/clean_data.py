import pandas as pd
import os

def process_raw_data():
    """
    Reads the Summary (for coordinates) and State data, merges them, 
    and saves to processed/ folder.
    """
    # 1. Load Station Coordinates (from your 'Summary.csv' or 'MS with lat and Lon')
    summary_df = pd.read_csv('../../data/raw/Air Pollution Data for Dashboard copy.xlsx - Summary.csv')
    stations = summary_df[['Monitoring Station', 'Latitude', 'Longitude']].dropna()
    stations.to_csv('../../data/processed/stations.csv', index=False)

    # 2. Load and merge State AQI Data (Example: combining Delhi and Maharashtra)
    # In reality, you will loop through all your state CSVs here
    df_mh = pd.read_csv('../../data/raw/Air Pollution Data for Dashboard copy.xlsx - Maharashtra.csv')
    df_dl = pd.read_csv('../../data/raw/Air Pollution Data for Dashboard copy.xlsx - Delhi.csv')
    
    combined_df = pd.concat([df_mh, df_dl], ignore_index=True)
    
    # 3. Clean Date and sort
    combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
    combined_df = combined_df.dropna(subset=['Date', 'AQI'])
    combined_df = combined_df.sort_values(['Monitoring Station', 'Date'])
    
    # Save processed data
    combined_df.to_csv('../../data/processed/cleaned_data.csv', index=False)
    print("Data cleaning complete. Saved to processed/")

if __name__ == "__main__":
    process_raw_data()