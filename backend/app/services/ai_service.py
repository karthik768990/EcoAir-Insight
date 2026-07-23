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
    Generate environmental insights using Gemini.
    """
    prompt = f"""
You are an expert environmental scientist. Provide a highly professional, objective, and concise analysis based on the following air quality data:

Location Context: Coordinates only (do not guess city names).
AQI: {data.get("aqi")}
PM2.5: {data.get("pm25")}
PM10: {data.get("pm10")}
Dominant Pollutant: {data.get("pollutant")}

Structure your response with the following headers:
1. Causes of Pollution
2. Health Risks
3. Recommended Actions
4. Future Outlook

Constraints:
- Maintain a formal, scientific tone.
- Do not use emojis or exclamation marks.
- Be extremely concise (maximum 3 sentences per section).
- Focus only on the provided data and scientifically established facts.
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