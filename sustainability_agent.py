# agents/sustainability_agent.py

class SustainabilityAgent:
    def evaluate_crops(self, crop_list):
        # Dummy logic for now
        eco_scores = {crop: 0.8 for crop in crop_list}
        return {
            "eco_friendly_crops": crop_list[:2],
            "eco_scores": eco_scores
        }
