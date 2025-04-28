# agents/crop_data.py
from .data_processor import load_crop_data

def get_crop_data(soil_ph=7.5, soil_moisture=30.0, soil_nitrogen=50.0):
    return load_crop_data()

CROP_DATA = get_crop_data()  # Default WISE3 averages