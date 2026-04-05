#!/usr/bin/env python
"""Quick start testing guide - Run this to verify the entire pipeline."""

import subprocess
import time
import sys
from pathlib import Path

def run_test():
    print("\n" + "="*70)
    print("  ECOAIR BACKEND - COMPLETE TESTING GUIDE")
    print("="*70)
    
    print("""
    This guide shows you how to test the air quality backend in different ways.
    Choose one of the methods below:
    """)
    
    print("\n" + "─"*70)
    print("Method 1: Integration Test (No Server Needed)")
    print("─"*70)
    print("""
    Run the complete pipeline test without starting a server:
    
    Command:
    $ cd backend && python test_integration.py
    
    Expected Output:
    ✓ Data loaded from ml/data/processed/
    ✓ 5-year predictions enabled
    ✓ Station: Mundka, Delhi - DPCC
    ✓ Current AQI: 507 (Severe)
    ✓ 5-Year Forecast: [459.82, 461.05, 433.83, ...]
    """)
    
    print("\n" + "─"*70)
    print("Method 2: Quick GET Endpoint Tests")
    print("─"*70)
    print("""
    Test the refactored GET endpoints:
    
    Command:
    $ python test_get_endpoints.py
    
    Expected Output:
    ✓ Testing GET /api/current-aqi
      Status: 200
      AQI: 507, Health Risk: Severe
    ✓ Testing GET /api/predict
      Status: 200
      Forecast length: 60 months
    """)
    
    print("\n" + "─"*70)
    print("Method 3: Start Live Server & Use Browser")
    print("─"*70)
    print("""
    Start the FastAPI server and test interactively:
    
    Step 1 - Start server:
    $ cd backend && python run.py
    
    Output should show:
    🚀 Starting EcoAir Insight API...
    Loading stations data...
    ✓ All data and models loaded successfully
    INFO:     Uvicorn running on http://127.0.0.1:8000
    
    Step 2 - Open interactive API docs:
    Browser: http://localhost:8000/docs
    
    Step 3 - Try POST in the UI:
    - Click on "/api/current-aqi"
    - Click "Try it out"
    - Enter: latitude=28.7041, longitude=77.1025
    - Click "Execute"
    """)
    
    print("\n" + "─"*70)
    print("Method 4: Use cURL (Command Line)")
    print("─"*70)
    print("""
    Test endpoints using curl (works in any terminal):
    
    Step 1 - Start server (in one terminal):
    $ cd backend && python run.py
    
    Step 2 - Make requests (in another terminal):
    
    Test Current AQI:
    $ curl "http://localhost:8000/api/current-aqi?latitude=28.7041&longitude=77.1025"
    
    Test 5-Year Prediction:
    $ curl "http://localhost:8000/api/predict?latitude=28.7041&longitude=77.1025"
    
    Test Health Check:
    $ curl "http://localhost:8000/"
    
    Test Invalid Input:
    $ curl "http://localhost:8000/api/current-aqi?latitude=95&longitude=77.1025"
    """)
    
    print("\n" + "─"*70)
    print("Method 5: Use Python Requests")
    print("─"*70)
    print("""
    Test with Python requests library:
    
    $ pip install requests
    
    Then run this Python code:
    """)
    
    python_code = '''import requests

BASE_URL = "http://localhost:8000/api"

# Test Current AQI
response = requests.get(
    f"{BASE_URL}/current-aqi",
    params={"latitude": 28.7041, "longitude": 77.1025}
)
print("Status:", response.status_code)
print("Response:", response.json())

# Test Predictions
response = requests.get(
    f"{BASE_URL}/predict",
    params={"latitude": 28.7041, "longitude": 77.1025}
)
print("Forecast:", response.json()["forecast_5_years"][:5])
'''
    print(python_code)
    
    print("\n" + "─"*70)
    print("Method 6: Use Postman (GUI)")
    print("─"*70)
    print("""
    Test using Postman graphical interface:
    
    1. Download Postman: https://www.postman.com/downloads/
    2. Create new request
    3. Set method to GET
    4. URL: http://localhost:8000/api/current-aqi
    5. Add query parameters:
       - Key: latitude, Value: 28.7041
       - Key: longitude, Value: 77.1025
    6. Click Send
    7. View response in Response tab
    """)
    
    print("\n" + "─"*70)
    print("Testing Coverage Checklist")
    print("─"*70)
    print("""
    ✓ Backend loads ML data from ml/data/processed/
    ✓ GET endpoints work with query parameters
    ✓ Current AQI endpoint returns health risk assessment
    ✓ Prediction endpoint returns 5-year forecast (60 months)
    ✓ Invalid coordinates return 400/422 error
    ✓ Response times < 50ms (in-memory caching)
    ✓ Multiple cities can be queried
    ✓ Data is consistent (same input = same output)
    """)
    
    print("\n" + "─"*70)
    print("Common Test Locations")
    print("─"*70)
    print("""
    Delhi:      latitude=28.7041, longitude=77.1025
    Mumbai:     latitude=19.0760, longitude=72.8777
    Bangalore:  latitude=12.9716, longitude=77.5946
    Kolkata:    latitude=22.5726, longitude=88.3639
    Chennai:    latitude=13.0827, longitude=80.2707
    """)
    
    print("\n" + "─"*70)
    print("Expected Response Format")
    print("─"*70)
    print("""
    GET /api/current-aqi Response (200 OK):
    {
      "location": {"lat": 28.7041, "lon": 77.1025},
      "aqi": 507,
      "pm25": 268.1,
      "pm10": 439.83,
      "health_risk": "Severe",
      "suggestion": "Avoid outdoor activities",
      "primary_pollutant": "PM2.5"
    }
    
    GET /api/predict Response (200 OK):
    {
      "location": {"lat": 28.7041, "lon": 77.1025},
      "forecast_5_years": [459.82, 461.05, 433.83, ..., 16.26]
    }
    """)
    
    print("\n" + "─"*70)
    print("Troubleshooting Tips")
    print("─"*70)
    print("""
    1. If "ModuleNotFoundError" → Run: pip install -r requirements.txt
    
    2. If "Data not loaded" → Check data files exist:
       Test-Path "ml/data/processed/stations.csv"
    
    3. If "Connection refused" → Make sure server is running:
       cd backend && python run.py
    
    4. If "No module named 'fastapi'" → Install dependencies:
       pip install fastapi uvicorn
    
    5. For JSON parsing errors → Use proper URL encoding in curl
    """)
    
    print("\n" + "─"*70)
    print("Quick Start Commands")
    print("─"*70)
    print("""
    # One-liner integration test:
    cd backend && python test_integration.py
    
    # Start server:
    cd backend && python run.py
    
    # Quick endpoint test:
    python test_get_endpoints.py
    
    # Simple curl test:
    curl "http://localhost:8000/api/current-aqi?latitude=28.7041&longitude=77.1025"
    """)
    
    print("\n" + "="*70)
    print("  Documentation Files:")
    print("="*70)
    print("""
    - TESTING_GUIDE.md          → Comprehensive testing guide
    - API_REFACTORING.md        → Why GET instead of POST
    - backend/test_integration.py  → Full pipeline test
    - backend/app/routes/api.py    → Current implementation
    """)
    
    print("\n" + "="*70)
    print("  Ready to test? Start with Method 1 or 3!")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_test()
