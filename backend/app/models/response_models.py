from pydantic import BaseModel
from typing import List, Optional


class LocationRequest(BaseModel):
    latitude: float
    longitude: float


class CurrentAQIResponse(BaseModel):
    location: dict
    aqi: int
    pm25: float
    pm10: float
    health_risk: str
    suggestion: str
    primary_pollutant: Optional[str] = None


class PredictionResponse(BaseModel):
    location: dict
    forecast_5_years: List[int]


class ErrorResponse(BaseModel):
    detail: str
