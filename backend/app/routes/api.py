from fastapi import APIRouter, HTTPException
from models.response_models import (
    LocationRequest,
    CurrentAQIResponse,
    PredictionResponse
)
from services.aqi_service import get_current_aqi_info, get_prediction_data
from services.location_service import validate_coordinates

router = APIRouter(prefix="/api", tags=["air-quality"])


@router.post("/current-aqi", response_model=CurrentAQIResponse)
def fetch_current_aqi(location: LocationRequest):
    """Get current AQI and health information for a location."""
    try:
        is_valid, error_msg = validate_coordinates(location.latitude, location.longitude)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        aqi_info = get_current_aqi_info(location.latitude, location.longitude)
        
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


@router.post("/predict", response_model=PredictionResponse)
def predict_aqi_trend(location: LocationRequest):
    """Get 5-year AQI predictions for a location."""
    try:
        is_valid, error_msg = validate_coordinates(location.latitude, location.longitude)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        pred_info = get_prediction_data(location.latitude, location.longitude)
        
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