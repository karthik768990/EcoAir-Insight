from pathlib import Path

# resolve path from backend/app/core/config.py -> backend -> EcoAir-Insight
BACKEND_DIR = Path(__file__).parent.parent.parent  # config.py parent parents: core -> app -> backend
BASE_DIR = BACKEND_DIR.parent  # backend -> EcoAir-Insight

# ML folder paths (at EcoAir-Insight level)
ML_DIR = BASE_DIR / "ml"
ML_DATA_DIR = ML_DIR / "data" / "processed"
ML_MODEL_DIR = ML_DIR / "models"

# Data file paths (sourced from ml folder)
STATIONS_CSV = ML_DATA_DIR / "stations.csv"
AQI_CSV = ML_DATA_DIR / "cleaned_data.csv"
PREDICTIONS_CSV = ML_DATA_DIR / "predictions_5yr_advanced.csv"

# ML Model path
MODEL_PATH = ML_MODEL_DIR / "saved_model.pkl"
