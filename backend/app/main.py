from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.health_service import get_aqi_health_info
from app.services.location_service import find_nearest_station
from app.services.aqi_service import get_current_aqi
from app.services.prediction_service import get_prediction
from app.services.ai_service import generate_ai_insights
from app.services.pollutant_analysis_service import analyze_pollutants


app = FastAPI()

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
    pollutant_analysis = analyze_pollutants(current)
    prediction = get_prediction(station)
    health = get_aqi_health_info(current["aqi"])

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