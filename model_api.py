from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib
import os

print("🚀 Flask API file is running...")

# Load model and scaler
model_path = os.path.join("..", "models", "lstm_cnn_model.h5")
scaler_path = os.path.join("..", "models", "scaler.pkl")

print("📂 Loading model...")
model = load_model(model_path)
print("✅ Model loaded.")

print("📂 Loading scaler...")
scaler = joblib.load(scaler_path)
print("✅ Scaler loaded.")

app = Flask(__name__)
print("🧠 Flask app created.")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = np.array(data["features"]).reshape(1, -1)

        features_scaled = scaler.transform(features)
        features_reshaped = features_scaled.reshape(1, 1, -1)

        prediction = model.predict(features_reshaped)[0][0]
        result = int(prediction > 0.5)

        return jsonify({"prediction": result, "score": float(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("✅ Starting Flask app on http://127.0.0.1:5000 ...")
    app.run(debug=True)
