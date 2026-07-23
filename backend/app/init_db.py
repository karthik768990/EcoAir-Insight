import os
from app.database import engine, Base
# Import all models here so metadata is registered
from app.models import Station, HistoricAQI, Prediction

def init_db():
    # Only create tables if they don't exist
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()
