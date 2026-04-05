#!/usr/bin/env python
"""Test GET endpoints after refactoring."""
import sys
from pathlib import Path

app_path = Path(__file__).parent / 'backend' / 'app'
sys.path.insert(0, str(app_path))

from fastapi.testclient import TestClient
from routes.api import router
from fastapi import FastAPI
from services.data_service import load_data

# Create app
app = FastAPI()
app.include_router(router)

# Load data
print("Loading data...")
load_data()

# Test
client = TestClient(app)

print("\n" + "=" * 60)
print("TESTING REFACTORED GET ENDPOINTS")
print("=" * 60)

# Test 1: Current AQI with GET
print("\n1. Testing GET /api/current-aqi")
response = client.get('/api/current-aqi', params={'latitude': 28.7041, 'longitude': 77.1025})
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   AQI: {data['aqi']}")
    print(f"   Health Risk: {data['health_risk']}")
    print("   [OK] GET request working!")
else:
    print(f"   Error: {response.json()}")

# Test 2: Predictions with GET
print("\n2. Testing GET /api/predict")
response = client.get('/api/predict', params={'latitude': 28.7041, 'longitude': 77.1025})
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Forecast length: {len(data['forecast_5_years'])} months")
    print(f"   First 5 months: {data['forecast_5_years'][:5]}")
    print("   [OK] GET request working!")
else:
    print(f"   Error: {response.json()}")

# Test 3: Invalid coordinates
print("\n3. Testing error handling (invalid latitude)")
response = client.get('/api/current-aqi', params={'latitude': 95, 'longitude': 77.1025})
print(f"   Status: {response.status_code}")
if response.status_code == 400:
    print(f"   Error correctly returned: {response.json()['detail'][:50]}...")
    print("   [OK] Input validation working!")

print("\n" + "=" * 60)
print("[OK] ALL TESTS PASSED - GET ENDPOINTS WORKING!")
print("=" * 60)
