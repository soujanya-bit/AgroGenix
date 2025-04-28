# agents/sustainability_agent.py
from .crop_data import CROP_DATA

class SustainabilityAgent:
    def evaluate_crops(self, crop_list):
        eco_scores = {
            crop["name"]: crop["sustainability_score"]
            for crop in CROP_DATA if crop["name"] in crop_list
        }
        eco_friendly_crops = [
            crop for crop in crop_list
            if eco_scores.get(crop, 0) > 0.7
        ]
        return {
            "eco_friendly_crops": eco_friendly_crops or crop_list[:1],
            "eco_scores": eco_scores
        }