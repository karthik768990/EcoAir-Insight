import pandas as pd
import re

def norm(t): return re.sub(r'[^a-z0-9 ]', '', str(t).lower().strip())

# Load datasets
preds = pd.read_csv('../../../ml/data/processed/predictions_5yr_advanced.csv')
news = pd.read_csv('../../../ml/data/processed/new_stations_data.csv')

# Get unique new stations with coordinates
uniques = news.drop_duplicates(subset=['STATION     NAME']).copy()
uniques['Latitude'] = pd.to_numeric(uniques['Latitude'], errors='coerce')
uniques['Longitude'] = pd.to_numeric(uniques['Longitude'], errors='coerce')
uniques = uniques.dropna(subset=['Latitude', 'Longitude'])

# Get normalized prediction stations
pred_stations_norm = set(preds['Monitoring Station'].apply(norm))

# Find which unique new stations are in the predictions
uniques['norm'] = uniques['STATION     NAME'].apply(norm)
working_new_stations = uniques[uniques['norm'].isin(pred_stations_norm)]

# Write to markdown
out_path = r'C:\Users\Karthik Tamarapalli\.gemini\antigravity\brain\664ca33b-2000-4220-8e8b-d254fb9f4eb4\new_stations_with_predictions.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# New Stations with 5-Year Predictions\n\n')
    f.write(f'There are {len(working_new_stations)} new stations from the master sheet that have valid coordinates and successfully integrated 5-year predictions.\n\n')
    f.write('| Station Name | Latitude | Longitude |\n')
    f.write('|--------------|----------|-----------|\n')
    for _, row in working_new_stations.iterrows():
        f.write(f"| {row['STATION     NAME']} | {row['Latitude']} | {row['Longitude']} |\n")

print(f'Successfully generated artifact with {len(working_new_stations)} stations.')
