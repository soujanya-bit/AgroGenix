# agents/soil_analyzer.py
from .crop_data import get_crop_data

class SoilAnalyzer:
    rainfall_map = {'Low': 300, 'Medium': 700, 'High': 1200}  # Class-level mapping
    
    def __init__(self, soil_type, rainfall, season, priority):
        # Load crop data with WISE3 averages
        self.crop_data = get_crop_data(
            soil_ph=7.5,  # Average from WISE3
            soil_moisture=30.0,  # Estimated average
            soil_nitrogen=50.0  # Estimated average
        )
        self.soil_type = soil_type
        self.rainfall = rainfall
        self.season = season
        self.priority = priority
        # Store explainable context
        self.weather = next((crop for crop in self.crop_data), {}).get('current_temp', 25.0), next((crop for crop in self.crop_data), {}).get('current_precip', 0.0)
        self.soil_ph = next((crop for crop in self.crop_data), {}).get('soil_ph', 7.5)
        self.soil_clay = next((crop for crop in self.crop_data), {}).get('soil_clay', 29)
        self.best_crop_name = None  # Initialize to store the best crop name

    def analyze(self):
        rainfall_value = self.rainfall_map[self.rainfall]
        
        # Map soil type to expected clay percentage
        soil_expectations = {
            'Sandy': {'clay_max': 20},
            'Clay': {'clay_min': 40},
            'Loamy': {'clay_min': 20, 'clay_max': 30},
            'Black': {'clay_min': 30, 'clay_max': 60}
        }
        expected_soil = soil_expectations[self.soil_type]
        
        suitable_crops = []
        for crop in self.crop_data:
            # Check season compatibility
            if self.season not in crop['seasons']:
                continue
                
            # Check rainfall compatibility
            is_rainfall_suitable = crop['precipitation_min'] <= rainfall_value <= crop['precipitation_max']
            
            # Check soil compatibility (using clay percentage from WISE3)
            is_soil_suitable = True
            if 'clay_min' in expected_soil and crop['soil_clay'] < expected_soil['clay_min']:
                is_soil_suitable = False
            if 'clay_max' in expected_soil and crop['soil_clay'] > expected_soil['clay_max']:
                is_soil_suitable = False
                
            # Base score from data_processor
            score = crop['sustainability_score']
            
            # Adjust score based on user inputs
            if not is_rainfall_suitable:
                score *= 0.5
            if not is_soil_suitable:
                score *= 0.7
                
            # Adjust for priority
            if self.priority == 'High Profit':
                price_factor = crop['market_price'] / 100
                score = score * 0.5 + price_factor * 0.5
            # Else, sustainability is the focus
            
            suitable_crops.append((crop['name'], score))
        
        # Sort and get the best crop
        suitable_crops.sort(key=lambda x: x[1], reverse=True)
        best_crop = suitable_crops[0] if suitable_crops else ("No suitable crop", 0.0)
        self.best_crop_name = best_crop[0]  # Store the best crop name
        return best_crop

    def get_explanation(self):
        crop_name = self.best_crop_name  # Use stored crop name
        temp, precip = self.weather
        explanation = f"Here's why we recommend {crop_name}:\n"
        explanation += f"- Your **{self.soil_type} soil** has {self.soil_clay:.1f}% clay, which is good for growing {crop_name}.\n"
        explanation += f"- **{self.rainfall} rainfall** (~{self.rainfall_map[self.rainfall]}mm) is enough for {crop_name} in your area.\n"
        explanation += f"- The **{self.season} season** is the right time to plant {crop_name}.\n"
        explanation += f"- You chose **{self.priority}**, so we picked {crop_name} to {'maximize your earnings' if self.priority == 'High Profit' else 'be sustainable and eco-friendly'}.\n"
        explanation += f"- Current conditions (Temp: {temp}°C, Rain: {precip}mm, pH: {self.soil_ph}) also support this choice."
        return explanation