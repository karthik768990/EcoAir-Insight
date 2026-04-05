from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.location_service import find_nearest_station
from app.services.aqi_service import get_current_aqi
from app.services.prediction_service import get_prediction

app = FastAPI()

# CORS (already added earlier but keeping clean)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/analysis")
def get_analysis(lat: float, lon: float):
    # 🔥 Step 1: Find station
    station = find_nearest_station(lat, lon)

    if not station:
        return {"error": "No station found"}

    # 🔥 Step 2: Get current AQI
    current = get_current_aqi(station)

    # 🔥 Step 3: Get predictions
    prediction = get_prediction(station)

    return {
        "station": station,
        "current": current,
        "prediction": prediction
    }