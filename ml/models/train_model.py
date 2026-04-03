import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

def train_and_predict():
    """
    Trains a model per station and pre-calculates the next 12 months.
    """
    df = pd.read_csv('../../data/processed/cleaned_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    predictions = []
    
    # Train a simple trendline model for each station
    for station, group in df.groupby('Monitoring Station'):
        group = group.sort_values('Date')
        group['Month_Index'] = np.arange(len(group))
        
        X = group[['Month_Index']]
        y = group['AQI']
        
        if len(group) < 10: continue # Skip if not enough data
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 12 months
        last_idx = group['Month_Index'].max()
        future_X = pd.DataFrame({'Month_Index': np.arange(last_idx + 1, last_idx + 13)})
        future_aqi = model.predict(future_X)
        
        for i, pred_aqi in enumerate(future_aqi):
            predictions.append({
                "Monitoring Station": station,
                "Month_Ahead": i + 1,
                "Predicted_AQI": round(pred_aqi, 2)
            })
            
    # Save predictions so the backend can serve them instantly
    pred_df = pd.DataFrame(predictions)
    pred_df.to_csv('../../data/processed/predictions_1yr.csv', index=False)
    print("Model trained and predictions saved!")

if __name__ == "__main__":
    train_and_predict()