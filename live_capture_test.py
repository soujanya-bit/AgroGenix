# wifi-ids-project/live_capture_test.py

import pyshark
import requests
import joblib
import time
from backend.utils.feature_extractor import extract_features

# Load the same scaler you used when training
scaler = joblib.load('backend/models/scaler.pkl')

# Flask API URL
API_URL = 'http://127.0.0.1:5000/predict'

# Use the "wifidump.exe" interface on Windows
interface =  r'\Device\NPF_{D2B920B6-9951-4D96-A87F-1F2D70832094}'

print(f"📡 Listening on interface: {interface}")
cap =  pyshark.LiveCapture(interface=interface)

for pkt in cap.sniff_continuously():
    # ① First: print a basic packet notice to confirm capture
    try:
        print("⚡ Packet captured:", pkt.highest_layer, pkt.length)
    except:
        print("⚡ Packet captured (unable to parse summary)")

    # ② Then try to extract features
    features = extract_features(pkt)
    if features:
        # Scale the 78-element vector
        norm = scaler.transform([features])
        # Send to your Flask model
        try:
            response = requests.post(API_URL, json={"features": norm[0].tolist()})
            result = response.json()
            print(f"    🔍 Prediction: {result['prediction']}, Score: {result.get('score', 'N/A')}")
        except Exception as api_e:
            print("    ❌ API error:", api_e)

    time.sleep(0.2)  # small delay

