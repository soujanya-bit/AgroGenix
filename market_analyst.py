# agents/market_analyst.py
from .crop_data import CROP_DATA

class MarketAnalyst:
    def predict_profit(self, crop_list):
        profits = {}
        for crop_name in crop_list:
            crop = next((c for c in CROP_DATA if c["name"] == crop_name), None)
            if crop:
                # Use market_price (USD/ton) and assume 5 tons/ha yield
                profits[crop_name] = crop["market_price"] * 5  # USD/ha
            else:
                profits[crop_name] = 1000  # Fallback profit
        best_crop = max(profits, key=profits.get, default=crop_list[0]) if profits else crop_list[0]
        return {
            "profit_estimates": profits,
            "best_crop": best_crop
        }