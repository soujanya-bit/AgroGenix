class SoilAnalyzer:
    def analyze(self, soil_type):
        if soil_type == "Sandy":
            return ["Pearl Millet", "Groundnut"]
        elif soil_type == "Clay":
            return ["Wheat", "Rice"]
        else:
            return ["Wheat", "Soybean"]
