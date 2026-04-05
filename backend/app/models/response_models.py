from pydantic import BaseModel
from typing import List, Optional


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
    forecast_5_years: List[float]  # Changed from int to float for accuracy


class ErrorResponse(BaseModel):
    detail: str
