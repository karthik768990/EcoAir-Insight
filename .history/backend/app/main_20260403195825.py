from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api

app = FastAPI(title="EcoAir Insight API")

# Allow React to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routes
app.include_router(api.router)

@app.get("/")
def home():
    return {"message": "EcoAir API is running"}d