# backend/app/services/pollutant_analysis_service.py

def get_pollutant_standards():
    """
    CPCB-based safe limits (µg/m3)
    """
    return {
        "pm25": 60,
        "pm10": 100,
        "no2": 80,
        "so2": 80,
        "co": 2,        # mg/m3 (handled separately)
        "ozone": 100
    }


def analyze_single_pollutant(name, value, standard):
    """
    Analyze a single pollutant
    """
    if value is None:
        return None

    try:
        value = float(value)
    except:
        return None

    ratio = value / standard if standard else 0

    if ratio <= 1:
        status = "Safe"
    elif ratio <= 1.5:
        status = "Moderate"
    else:
        status = "High"

    return {
        "name": name.upper(),
        "value": round(value, 2),
        "standard": standard,
        "ratio": round(ratio, 2),
        "status": status
    }


def analyze_pollutants(aqi_data: dict):
    """
    Main function to analyze all pollutants
    """

    standards = get_pollutant_standards()

    pollutants = {
        "pm25": aqi_data.get("pm25"),
        "pm10": aqi_data.get("pm10"),
        "no2": aqi_data.get("no2"),
        "so2": aqi_data.get("so2"),
        "co": aqi_data.get("co"),
        "ozone": aqi_data.get("ozone"),
    }

    analysis_results = {}

    max_ratio = -1
    major_pollutant = None

    for key, value in pollutants.items():
        if value is None:
            continue

        standard = standards.get(key)
        result = analyze_single_pollutant(key, value, standard)

        if result:
            analysis_results[key] = result

            # 🔥 Find dominant pollutant
            if result["ratio"] > max_ratio:
                max_ratio = result["ratio"]
                major_pollutant = result

    # 🔥 Explanation logic
    explanation = None
    if major_pollutant:
        explanation = (
            f"{major_pollutant['name']} is the dominant pollutant because its "
            f"concentration ({major_pollutant['value']} µg/m³) exceeds the safe limit "
            f"({major_pollutant['standard']}) by a factor of {major_pollutant['ratio']}. "
            f"This makes it the most significant contributor to the AQI."
        )

    return {
        "pollutants": analysis_results,
        "major_pollutant": major_pollutant,
        "explanation": explanation
    }