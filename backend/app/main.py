from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routes.api import router as api_router
from app.services.health_service import get_aqi_health_info
from app.services.location_service import find_nearest_station
from app.services.aqi_service import get_current_aqi
from app.services.prediction_service import get_prediction
from app.services.ai_service import generate_ai_insights
from app.services.pollutant_analysis_service import analyze_pollutants
from app.init_db import init_db
from app.database import get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get('/')
def get_hotroute():
    return {
        "status_code": 200,
        "health": "ok"
    }

@app.get("/analysis")
def get_analysis(lat: float, lon: float, db: Session = Depends(get_db)):
    station = find_nearest_station(lat, lon, db)
    if not station:
        return {"error": "No station found near these coordinates."}

    current = get_current_aqi(station, db)
    pollutant_analysis = analyze_pollutants(current)
    prediction = get_prediction(station, db)
    health = get_aqi_health_info(current.get("aqi", 0))

    ai = generate_ai_insights({
        **current,
        "station": station,
        "lat": lat,
        "lon": lon,
        "city": current.get("city"),
        "pollutant": current.get("pollutant")
    })

    return {
        "station": station,
        "current": {
            **current,
            "pollutants": pollutant_analysis["pollutants"],
            "major_pollutant": pollutant_analysis["major_pollutant"],
            "explanation": pollutant_analysis["explanation"]
        },
        "prediction": prediction,
        "health": health,
        "ai_insights": ai
    }