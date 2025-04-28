# agents/market_analyst.py

class MarketAnalyst:
    def predict_profit(self, crop_list):
        # Dummy logic for now
        profits = {crop: 10000 for crop in crop_list}
        return {
            "profit_estimates": profits,
            "best_crop": crop_list[0]
        }
