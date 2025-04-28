# agents/data_processor.py
import pandas as pd
import os
import requests

def load_crop_data():
    # Load WISE3 soil data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wise_path = os.path.join(base_dir, 'data', 'WISE3_HORIZON.xlsx')
    wise_df = pd.read_excel(wise_path)
    
    # Filter top horizon and handle missing values
    wise_top = wise_df[wise_df['HONU'] == 1].copy()
    wise_top['PHH2O'] = wise_top['PHH2O'].fillna(wise_top['PHH2O'].mean())
    wise_top['SAND'] = wise_top['SAND'].fillna(wise_top['SAND'].mean())
    wise_top['SILT'] = wise_top['SILT'].fillna(wise_top['SILT'].mean())
    wise_top['CLAY'] = wise_top['CLAY'].fillna(wise_top['CLAY'].mean())
    wise_top['EXK'] = wise_top['EXK'].fillna(wise_top['EXK'].mean())  # Potassium proxy
    
    # Aggregate average soil properties (simplified for demo)
    avg_soil = {
        'ph': wise_top['PHH2O'].mean(),
        'sand': wise_top['SAND'].mean(),
        'silt': wise_top['SILT'].mean(),
        'clay': wise_top['CLAY'].mean(),
        'potassium': wise_top['EXK'].mean() * 39.1  # Convert to kg/ha (approx)
    }
    
    # Load crop price data
    csv_path = os.path.join(base_dir, 'data', 'icrisat_crop_data.csv')
    print(f"Loading CSV from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Available columns: {df.columns.tolist()}")
    
    crop_price_mapping = {
        'Rice': 'RICE HARVEST PRICE',
        'Paddy': 'PADDY HARVEST PRICE',
        'Wheat': 'WHEAT HARVEST PRICE',
        'Sorghum': 'SORGHUM HARVEST PRICE',
        'Pearl Millet': 'PEARL MILLET HARVEST PRICE',
        'Maize': 'MAIZE HARVEST PRICE',
        'Finger Millet': 'FINGER MILLET HARVEST PRICE',
        'Barley': 'BARLEY HARVEST PRICE',
        'Chickpea': 'CHICKPEA HARVEST PRICE',
        'Pigeonpea': 'PIGEONPEA HARVEST PRICE',
        'Groundnut': 'GROUNDNUT HARVEST PRICE',
        'Seasamum': 'SEASAMUM HARVEST PRICE',
        'Rape and Mustard': 'RAPE AND MUSTARD HARVEST PRICE',
        'Castor': 'CASTOR HARVEST PRICE',
        'Linseed': 'LINSEED HARVEST PRICE',
        'Sugarcane': 'SUGARCANE GUR HARVEST PRICE',
        'Cotton': 'COTTON KAPAS HARVEST PRICE'
    }
    key_crops = list(crop_price_mapping.keys())
    
    available_columns = df.columns.tolist()
    valid_price_columns = {}
    for crop, price_col in crop_price_mapping.items():
        matched_col = next((col for col in available_columns if price_col.lower().replace(' ', '') in col.lower().replace(' ', '')), None)
        if matched_col:
            valid_price_columns[crop] = matched_col
        else:
            print(f"Warning: No match found for {price_col}, skipping {crop}")
    
    if not valid_price_columns:
        raise ValueError(f"No valid price columns found. Available columns: {available_columns}")
    
    df = df.dropna(subset=list(valid_price_columns.values()))
    crop_stats = {}
    for crop, price_col in valid_price_columns.items():
        crop_stats[crop] = {
            'HARVEST_PRICE (Rs per Quintal)': df[price_col].mean(),
            'Harvested_Area': df[price_col].count()
        }
    
    crop_stats_df = pd.DataFrame.from_dict(crop_stats, orient='index').reset_index()
    crop_stats_df = crop_stats_df.rename(columns={'index': 'Crop'})
    
    # Fetch real-time weather data (Delhi, India)
    api_key = "6TSVKYLK3538MVZD4XFL93NW6"
    location = "Delhi,India"
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={api_key}&unitGroup=metric&contentType=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"API Response Status: {response.status_code}")
        print(f"API Response Text: {response.text[:500]}...")
        weather_data = response.json()
        current_temp = weather_data['days'][0]['temp']
        precipitation = weather_data['days'][0]['precip']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        current_temp = 25.0
        precipitation = 50.0
    except ValueError as e:
        print(f"Error parsing weather data: {e}")
        current_temp = 25.0
        precipitation = 50.0
    
    # Define crop requirements
    season_map = {
        'Rice': 'Summer', 'Paddy': 'Summer', 'Wheat': 'Winter', 'Sorghum': 'Summer',
        'Pearl Millet': 'Summer', 'Maize': 'Summer', 'Finger Millet': 'Summer',
        'Barley': 'Winter', 'Chickpea': 'Winter', 'Pigeonpea': 'Summer',
        'Groundnut': 'Summer', 'Seasamum': 'Summer', 'Rape and Mustard': 'Winter',
        'Castor': 'Summer', 'Linseed': 'Winter', 'Sugarcane': 'Summer', 'Cotton': 'Summer'
    }
    crop_requirements = {
        'Rice': {'precip_min': 1000, 'precip_max': 2000, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 20, 'potassium_min': 50},
        'Paddy': {'precip_min': 1000, 'precip_max': 2000, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 20, 'potassium_min': 50},
        'Wheat': {'precip_min': 300, 'precip_max': 700, 'temp_min': 5, 'temp_max': 25, 'ph_min': 6.0, 'ph_max': 8.0, 'clay_min': 10, 'potassium_min': 40},
        'Sorghum': {'precip_min': 400, 'precip_max': 800, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 8.0, 'clay_min': 10, 'potassium_min': 30},
        'Pearl Millet': {'precip_min': 300, 'precip_max': 600, 'temp_min': 25, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 20},
        'Maize': {'precip_min': 500, 'precip_max': 1000, 'temp_min': 18, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 15, 'potassium_min': 60},
        'Finger Millet': {'precip_min': 400, 'precip_max': 800, 'temp_min': 20, 'temp_max': 30, 'ph_min': 5.0, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 30},
        'Barley': {'precip_min': 300, 'precip_max': 600, 'temp_min': 5, 'temp_max': 25, 'ph_min': 6.0, 'ph_max': 8.0, 'clay_min': 10, 'potassium_min': 40},
        'Chickpea': {'precip_min': 300, 'precip_max': 600, 'temp_min': 15, 'temp_max': 30, 'ph_min': 6.0, 'ph_max': 8.0, 'clay_min': 10, 'potassium_min': 20},
        'Pigeonpea': {'precip_min': 500, 'precip_max': 1000, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 20},
        'Groundnut': {'precip_min': 500, 'precip_max': 1000, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.0, 'clay_min': 10, 'potassium_min': 30},
        'Seasamum': {'precip_min': 400, 'precip_max': 800, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 20},
        'Rape and Mustard': {'precip_min': 300, 'precip_max': 600, 'temp_min': 10, 'temp_max': 25, 'ph_min': 6.0, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 40},
        'Castor': {'precip_min': 500, 'precip_max': 1000, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 30},
        'Linseed': {'precip_min': 300, 'precip_max': 600, 'temp_min': 10, 'temp_max': 25, 'ph_min': 6.0, 'ph_max': 7.5, 'clay_min': 10, 'potassium_min': 30},
        'Sugarcane': {'precip_min': 1500, 'precip_max': 2500, 'temp_min': 20, 'temp_max': 35, 'ph_min': 6.0, 'ph_max': 8.0, 'clay_min': 20, 'potassium_min': 80},
        'Cotton': {'precip_min': 500, 'precip_max': 1200, 'temp_min': 20, 'temp_max': 35, 'ph_min': 5.5, 'ph_max': 7.5, 'clay_min': 15, 'potassium_min': 60}
    }
    
    # Build CROP_DATA with WISE3 soil and weather integration
    CROP_DATA = []
    for crop in key_crops:
        if crop in valid_price_columns:
            crop_row = crop_stats_df[crop_stats_df['Crop'] == crop].iloc[0]
            # Weather suitability
            is_temp_suitable = crop_requirements[crop]['temp_min'] <= current_temp <= crop_requirements[crop]['temp_max']
            is_precip_suitable = crop_requirements[crop]['precip_min'] <= (precipitation * 30) <= crop_requirements[crop]['precip_max']
            # Soil suitability from WISE3 averages
            is_ph_suitable = crop_requirements[crop]['ph_min'] <= avg_soil['ph'] <= crop_requirements[crop]['ph_max']
            is_clay_suitable = crop_requirements[crop]['clay_min'] <= avg_soil['clay']
            is_potassium_suitable = crop_requirements[crop]['potassium_min'] <= avg_soil['potassium']
            # Combined suitability score
            suitability_score = 0.8 if (is_temp_suitable and is_precip_suitable and is_ph_suitable and is_clay_suitable and is_potassium_suitable) else 0.4
            # Adjust score based on market price
            price_factor = (crop_row['HARVEST_PRICE (Rs per Quintal)'] / 10) / 100
            final_score = suitability_score * 0.7 + price_factor * 0.3
            CROP_DATA.append({
                'name': crop,
                'precipitation_min': crop_requirements[crop]['precip_min'],
                'precipitation_max': crop_requirements[crop]['precip_max'],
                'temperature_min': crop_requirements[crop]['temp_min'],
                'temperature_max': crop_requirements[crop]['temp_max'],
                'seasons': [season_map[crop]],
                'market_price': crop_row['HARVEST_PRICE (Rs per Quintal)'] / 10,
                'sustainability_score': final_score,
                'water_usage': crop_requirements[crop]['precip_min'] * 1.5,
                'current_temp': current_temp,
                'current_precip': precipitation,
                'soil_ph': avg_soil['ph'],
                'soil_clay': avg_soil['clay'],
                'soil_potassium': avg_soil['potassium']
            })
    
    print(f"CROP_DATA: {CROP_DATA}")
    return CROP_DATA