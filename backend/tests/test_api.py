import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
import os

# Use a test database
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_hotroute():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "health": "ok"}

def test_analysis_no_station():
    # Sending some random coordinates that don't match any station
    response = client.get("/analysis?lat=0.0&lon=0.0")
    # Our data_service haversine will pick the closest but since the DB is empty, it returns none
    assert response.status_code == 200
    assert response.json() == {"error": "No station found near these coordinates."}
