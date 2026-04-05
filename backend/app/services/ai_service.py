import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Explicitly check for the key to ensure fail-safe startup
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

def generate_ai_insights(data: dict) -> str:
    """
    Generate environmental insights using Gemini 1.5 Flash.
    """
    prompt = f"""
You are an environmental expert.

Given the air quality data:
AQI: {data.get("aqi")}
PM2.5: {data.get("pm25")}
PM10: {data.get("pm10")}
City: {data.get("city")}
Dominant Pollutant: {data.get("pollutant")}

Provide:
1. Causes of pollution
2. Health risks
3. Recommended actions
4. Future outlook

Keep response short and structured.
"""

    try:
        # The new SDK handles the routing and versioning automatically
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )

        return response.text

    except Exception as e:
        print(f"Gemini error: {e}")
        return "AI insights currently unavailable."