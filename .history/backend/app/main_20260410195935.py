from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.health_service import get_aqi_health_info
from app.services.location_service import find_nearest_station
from app.services.aqi_service import get_current_aqi
from app.services.prediction_service import get_prediction
from app.services.ai_service import generate_ai_insights



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
    station = find_nearest_station(lat, lon)

    current = get_current_aqi(station)
    prediction = get_prediction(station)
    health = get_aqi_health_info(current["aqi"])

    # 🔥 AI INSIGHTS
    ai = generate_ai_insights({
        **current,
        "city": current.get("city"),
        "pollutant": current.get("pollutant")
    })

    return {
        "station": station,
        "current": current,
        "prediction": prediction,
        "health": health,
        "ai_insights": ai
    }