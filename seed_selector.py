# agents/seed_selector.py
from .crop_data import CROP_DATA

class SeedSelector:
    def select_best_seed(self, soil_output, weather_output, market_output, sustainability_output, goal="High Profit"):
        viable_crops = set(soil_output["recommended_crops"]) & set(weather_output["suitable_crops"])
        if not viable_crops:
            viable_crops = set(soil_output["recommended_crops"])  # Fallback

        scores = {}
        for crop in viable_crops:
            crop_data = next((c for c in CROP_DATA if c["name"] == crop), None)
            if crop_data:
                profit = crop_data["market_price"] * 5  # Use market_price, assume 5 tons/ha
            else:
                profit = 1000  # Fallback
            eco_score = sustainability_output["eco_scores"].get(crop, 0.5)
            # Weight based on goal
            if goal == "High Profit":
                score = (profit / 2000) * 0.7 + eco_score * 0.3  # Prioritize profit
            else:  # Sustainability
                score = eco_score * 0.7 + (profit / 2000) * 0.3  # Prioritize eco-score
            scores[crop] = score

        final_crop = max(scores, key=scores.get, default=viable_crops.pop() if viable_crops else "Wheat")
        return {
            "final_recommendation": final_crop
        }