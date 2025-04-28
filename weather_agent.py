# agents/weather_agent.py
from .crop_data import CROP_DATA

class WeatherAgent:
    def assess_weather(self, season, rainfall_level):
        rainfall_map = {"Low": 400, "Medium": 700, "High": 1200}  # mm
        precipitation = rainfall_map.get(rainfall_level, 700)
        temperature = 20  # Default (dataset-based temp not available)
        
        suitable_crops = [
            crop["name"] for crop in CROP_DATA
            if (crop["precipitation_min"] <= precipitation <= crop["precipitation_max"] and
                crop["temperature_min"] <= temperature <= crop["temperature_max"] and
                season in crop["seasons"])
        ]
        weather_risk = "Low" if suitable_crops else "High"
        weather_score = 0.9 if suitable_crops else 0.4
        return {
            "weather_risk": weather_risk,
            "weather_score": weather_score,
            "suitable_crops": suitable_crops or ["Wheat"],
            "precipitation": precipitation,
            "temperature": temperature
        }