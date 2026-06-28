import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None

client = None


def _get_genai_client():
    global client
    if client is not None:
        return client

    if genai is None:
        return None

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Gemini client initialization failed: {e}")
        client = None

    return client

def generate_ai_insights(data: dict) -> str:
    """
    Generate environmental insights using Gemini 1.5 Flash.
    """
    prompt = f"""
You are an environmental expert.

Given the air quality data for the location is as follows:

AQI: {data.get("aqi")}
PM2.5: {data.get("pm25")}
PM10: {data.get("pm10")}
Dominant Pollutant: {data.get("pollutant")}

Provide:
1. Causes of pollution
2. Health risks
3. Recommended actions
4. Future outlook

Keep response short and structured. Focus strictly on the provided coordinates and DO NOT mention specific city names, as the user has selected a precise map location.
"""

    client = _get_genai_client()
    if client is None:
        return "AI insights currently unavailable."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print(f"Gemini error: {e}")
        return "AI insights currently unavailable."