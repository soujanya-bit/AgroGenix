# agents/explanation_agent.py

class ExplanationAgent:
    def generate_report(self, selected_crop, soil_output, weather_output, market_output, sustainability_output):
        soil_crops = soil_output["recommended_crops"]
        weather_crops = weather_output["suitable_crops"]
        profit = market_output["profit_estimates"].get(selected_crop, 1000)
        eco_score = sustainability_output["eco_scores"].get(selected_crop, 0.5)
        
        report = f"""
        We recommend **{selected_crop}** for your farm because:
        - **Soil Compatibility**: {selected_crop} thrives in your soil type, matching {soil_crops}.
        - **Weather Suitability**: It suits the {weather_output['weather_risk']} risk conditions and season.
        - **Market Potential**: Expected profit of ${profit} per hectare.
        - **Sustainability**: Eco-score of {eco_score:.2f}, indicating {'high' if eco_score > 0.7 else 'moderate'} environmental friendliness.
        """
        return report