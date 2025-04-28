# app.py
import streamlit as st
from agents.soil_analyzer import SoilAnalyzer
from agents.crop_data import get_crop_data
import matplotlib.pyplot as plt
import numpy as np

st.title("🌾 BioSeed Selector")
st.write("Powered by ICRISAT data (1966–present), covering 17 major Indian crops like Rice, Wheat, Maize, and Cotton.")
st.write("**Smart Crop Recommendation for Every Farmer**")
st.write("Answer a few simple questions to get the best crop recommendation based on your land and market conditions.")

st.subheader("Tell us about your field:")
soil_type = st.selectbox("🌱 What type of soil is your field?", ["Sandy", "Clay", "Loamy", "Black"])
rainfall = st.selectbox("☔ How is the rainfall in your area?", ["Low", "Medium", "High"])
season = st.selectbox("🌞 Which season are you planning to plant?", ["Summer", "Winter"])
priority = st.selectbox("🎯 What is your goal?", ["Sustainability", "High Profit"])

if st.button("⏳ Analyze my field"):
    try:
        analyzer = SoilAnalyzer(soil_type, rainfall, season, priority)
        best_crop, score = analyzer.analyze()
        
        st.subheader("Best Crop Recommendation")
        st.write(f"**{best_crop}** - Score: {score:.2f}")
        # Fetch market price from CROP_DATA
        crop_name = best_crop[0] if isinstance(best_crop, tuple) else best_crop
        market_price = next((crop['market_price'] for crop in get_crop_data() if crop['name'] == crop_name), 0)
        st.write(f"**Market Value**: ₹{market_price:.2f} per 10 quintals")
        st.write("This crop is recommended based on your soil type, rainfall, season, and goal.")
        
        # Display explanation
        st.subheader("Why This Crop?")
        st.write(analyzer.get_explanation())
        
        # Restore graph (bar chart of top 3 crop scores)
        suitable_crops = []
        for crop in analyzer.crop_data:
            if season in crop['seasons']:
                score = crop['sustainability_score']
                if priority == 'High Profit':
                    score = score * 0.5 + (crop['market_price'] / 100) * 0.5
                suitable_crops.append((crop['name'], score))
        suitable_crops.sort(key=lambda x: x[1], reverse=True)
        top_3 = suitable_crops[:3]
        
        names = [crop[0] for crop in top_3]
        scores = [crop[1] for crop in top_3]
        
        fig, ax = plt.subplots()
        ax.bar(names, scores, color=['#4CAF50', '#FF9800', '#2196F3'])
        ax.set_ylabel('Suitability Score')
        ax.set_title('Top 3 Crop Recommendations')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check your inputs and try again.")