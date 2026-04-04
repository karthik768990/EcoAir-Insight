from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
BASE_DIR = BACKEND_DIR.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

STATIONS_CSV = PROCESSED_DATA_DIR / "stations.csv"
AQI_CSV = PROCESSED_DATA_DIR / "cleaned_data.csv"
PREDICTIONS_CSV = PROCESSED_DATA_DIR / "predictions_1yr.csv"

ML_MODEL_DIR = BASE_DIR / "ml" / "models"
MODEL_PATH = ML_MODEL_DIR / "saved_model.pkl"
