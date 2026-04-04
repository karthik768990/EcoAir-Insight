from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api
from services.data_service import load_data, is_data_loaded

app = FastAPI(title="EcoAir Insight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)


@app.on_event("startup")
async def startup_event():
    """Load data when server starts."""
    print("🚀 Starting EcoAir Insight API...")
    try:
        load_data()
    except Exception as e:
        print(f"✗ Failed to load data: {e}")
        raise


@app.get("/")
def home():
    """Health check endpoint."""
    data_status = "loaded" if is_data_loaded() else "not loaded"
    return {
        "message": "EcoAir Insight API is running",
        "status": "healthy",
        "data": data_status
    }


@app.get("/health")
def health():
    """Kubernetes-style health endpoint."""
    if not is_data_loaded():
        return {"status": "unhealthy", "reason": "Data not loaded"}
    return {"status": "healthy"}