# agents/seed_selector.py

class SeedSelector:
    def select_best_seed(self, soil_output, weather_output, market_output, sustainability_output):
        # Dummy logic for now
        final_crop = market_output["best_crop"]
        return {
            "final_recommendation": final_crop
        }
