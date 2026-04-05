from fastapi import APIRouter, HTTPException, Query
from models.response_models import (
    CurrentAQIResponse,
    PredictionResponse
)
from services.aqi_service import get_current_aqi_info, get_prediction_data
from services.location_service import validate_coordinates

router = APIRouter(prefix="/api", tags=["air-quality"])


@router.get("/current-aqi", response_model=CurrentAQIResponse)
def fetch_current_aqi(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)")
):
    """Get current AQI and health information for a location.
    
    Query Parameters:
    - latitude: Geographic latitude (-90 to 90)
    - longitude: Geographic longitude (-180 to 180)
    
    Example: /api/current-aqi?latitude=28.7041&longitude=77.1025
    """
    try:
        is_valid, error_msg = validate_coordinates(latitude, longitude)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        aqi_info = get_current_aqi_info(latitude, longitude)
        
        return CurrentAQIResponse(
            location=aqi_info["location"],
            aqi=aqi_info["aqi"],
            pm25=aqi_info["pm25"],
            pm10=aqi_info["pm10"],
            health_risk=aqi_info["health_risk"],
            suggestion=aqi_info["suggestion"],
            primary_pollutant=aqi_info["primary_pollutant"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/predict", response_model=PredictionResponse)
def predict_aqi_trend(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)")
):
    """Get 5-year AQI predictions for a location.
    
    Query Parameters:
    - latitude: Geographic latitude (-90 to 90)
    - longitude: Geographic longitude (-180 to 180)
    
    Example: /api/predict?latitude=28.7041&longitude=77.1025
    """
    try:
        is_valid, error_msg = validate_coordinates(latitude, longitude)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        pred_info = get_prediction_data(latitude, longitude)
        
        return PredictionResponse(
            location=pred_info["location"],
            forecast_5_years=pred_info["forecast_5_years"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")