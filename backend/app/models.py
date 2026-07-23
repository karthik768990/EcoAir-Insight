from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from app.database import Base

class Station(Base):
    __tablename__ = "stations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    name_norm = Column(String, unique=True, index=True, nullable=False)
    city = Column(String, index=True)
    state = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
class HistoricAQI(Base):
    __tablename__ = "historic_aqi"
    
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, index=True)
    date = Column(DateTime, index=True, nullable=False)
    
    aqi = Column(Float)
    pm25 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    co = Column(Float)
    ozone = Column(Float)
    
    temp = Column(Float)
    rh = Column(Float)
    ws = Column(Float)

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, index=True)
    month_ahead = Column(Integer, nullable=False)
    
    predicted_aqi = Column(Float, nullable=False)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
