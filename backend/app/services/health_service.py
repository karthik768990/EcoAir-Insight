def get_aqi_health_info(aqi: float):
    """
    Returns AQI category, color, and health advice
    """

    if aqi is None:
        return {
            "category": "Unknown",
            "color": "#9e9e9e",
            "advice": "No data available."
        }

    if aqi <= 50:
        return {
            "category": "Good",
            "color": "#00e400",
            "advice": "Air quality is excellent. Enjoy outdoor activities."
        }

    elif aqi <= 100:
        return {
            "category": "Moderate",
            "color": "#ffff00",
            "advice": "Air quality is acceptable. Sensitive individuals should take care."
        }

    elif aqi <= 200:
        return {
            "category": "Unhealthy for Sensitive Groups",
            "color": "#ff7e00",
            "advice": "Children, elderly, and people with respiratory issues should limit outdoor exposure."
        }

    elif aqi <= 300:
        return {
            "category": "Unhealthy",
            "color": "#ff0000",
            "advice": "Everyone may experience health effects. Avoid outdoor activities."
        }

    elif aqi <= 400:
        return {
            "category": "Very Unhealthy",
            "color": "#8f3f97",
            "advice": "Health alert: serious health effects possible. Stay indoors."
        }

    else:
        return {
            "category": "Hazardous",
            "color": "#7e0023",
            "advice": "Emergency conditions. Avoid all outdoor exposure."
        }