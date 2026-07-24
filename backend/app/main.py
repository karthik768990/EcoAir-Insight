from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routes.api import router as api_router
from app.services.health_service import get_aqi_health_info
from app.services.location_service import find_nearest_station, find_nearest_station_with_data
from app.services.aqi_service import get_current_aqi
from app.services.prediction_service import get_prediction
from app.services.ai_service import generate_ai_insights
from app.services.pollutant_analysis_service import analyze_pollutants
from app.init_db import init_db
from app.database import get_db
import threading

is_migrating = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    global is_migrating
    init_db()
    
    # Check if DB is empty and run migration if needed
    import subprocess
    from app.database import SessionLocal
    from app.models import Station
    
    db = SessionLocal()
    try:
        import os
        station_count = db.query(Station).count()
        if station_count == 0 and not os.environ.get("TESTING"):
            print("Database is empty. Running initial migration...")
            is_migrating = True
            
            def run_migration():
                global is_migrating
                import os
                script_path = os.path.join(os.path.dirname(__file__), "../../ml/data_processing/migrate_to_db.py")
                if os.path.exists(script_path):
                    subprocess.run(["python", script_path])
                else:
                    # Docker path fallback
                    subprocess.run(["python", "/app/ml/data_processing/migrate_to_db.py"])
                print("Initial migration completed.")
                is_migrating = False

            # Run in a background thread so FastAPI can start immediately
            threading.Thread(target=run_migration, daemon=True).start()
    except Exception as e:
        print(f"Migration error during startup: {e}")
    finally:
        db.close()

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
    global is_migrating
    if is_migrating:
        return {"error": "Database is currently being populated with initial data. Please wait a minute and try again."}

    location_data = find_nearest_station_with_data(lat, lon, db)
    
    if location_data.get("data_unavailable"):
        if "error" in location_data:
            return {"error": location_data["error"]}
        return {"data_unavailable": True}

    station_obj = location_data["station"]
    station = station_obj.name
    
    current = get_current_aqi(station, db)
    if not current:
        return {"data_unavailable": True}
        
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
        "is_fallback": location_data.get("is_fallback", False),
        "distance_km": location_data.get("distance_km", 0),
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