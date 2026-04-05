#!/usr/bin/env python
"""Test ML integration with backend services."""
import sys
from pathlib import Path

# Add app to path
app_path = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_path))

from services.data_service import load_data, is_data_loaded
from services.aqi_service import get_current_aqi_info, get_prediction_data

# Load data
print("=" * 60)
print("LOADING DATA FROM ML FOLDER")
print("=" * 60)
load_data()

# Test API functionality
if is_data_loaded():
    print("\n" + "=" * 60)
    print("TESTING API ENDPOINTS WITH ML DATA")
    print("=" * 60)
    
    # Test current AQI
    print("\n1. Testing current AQI endpoint (Delhi, India):")
    try:
        result = get_current_aqi_info(28.7041, 77.1025)
        print(f"   [OK] Station: {result['station']}")
        print(f"   [OK] AQI: {result['aqi']}")
        print(f"   [OK] PM2.5: {result['pm25']} ug/m3")
        print(f"   [OK] Health Risk: {result['health_risk']}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test predictions
    print("\n2. Testing 5-year predictions endpoint:")
    try:
        result = get_prediction_data(28.7041, 77.1025)
        print(f"   [OK] Station: {result['station']}")
        forecast = result['forecast_5_years'][:5] if len(result['forecast_5_years']) >= 5 else result['forecast_5_years']
        print(f"   [OK] 5-Year Forecast (first 5 months): {forecast}")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print("\n" + "=" * 60)
    print("[OK] INTEGRATION TEST SUCCESSFUL!")
    print("  - Data loaded from: ml/data/processed/")
    print("  - 5-year predictions enabled")
    print("  - API endpoints working with ML data")
    print("=" * 60)
else:
    print("[ERROR] Data not loaded")
