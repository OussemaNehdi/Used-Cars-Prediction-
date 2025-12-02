from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import os
from datetime import datetime

# Initialize App
app = FastAPI(title="Tunisian Car Price Predictor")

# Add CORS middleware to allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # NextJS development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model and Encoders
MODEL_PATH = "car_price_model.pkl"
BRAND_ENCODER_PATH = "brand_encoder.pkl"
MODEL_ENCODER_PATH = "model_encoder.pkl"
FEATURE_NAMES_PATH = "feature_names.pkl"

model = None
brand_encoder = None
model_encoder = None
feature_names = None

# Load all necessary files
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully.")
else:
    print("❌ WARNING: car_price_model.pkl not found. Run training_xmodel.py first.")

if os.path.exists(BRAND_ENCODER_PATH):
    with open(BRAND_ENCODER_PATH, 'rb') as f:
        brand_encoder = pickle.load(f)
    print("✓ Brand encoder loaded successfully.")
else:
    print("❌ WARNING: brand_encoder.pkl not found. Run training_model.py first.")

if os.path.exists(MODEL_ENCODER_PATH):
    with open(MODEL_ENCODER_PATH, 'rb') as f:
        model_encoder = pickle.load(f)
    print("✓ Model encoder loaded successfully.")
else:
    print("❌ WARNING: model_encoder.pkl not found. Run training_model.py first.")

if os.path.exists(FEATURE_NAMES_PATH):
    with open(FEATURE_NAMES_PATH, 'rb') as f:
        feature_names = pickle.load(f)
    print(f"✓ Feature names loaded successfully: {feature_names}")
else:
    print("❌ WARNING: feature_names.pkl not found. Run training_model.py first.")

# Define Input Structure (What frontend sends us)
class CarPredictionInput(BaseModel):
    year: int        # e.g., 2020
    brand: str       # e.g., "Kia"
    model: str       # e.g., "Rio"
    mileage: int     # e.g., 85000
    cv: int          # e.g., 5
    fuel_type: str   # e.g., "Essence" or "Diesel"
    transmission: str # e.g., "Manuelle" or "Automatique"

@app.get("/")
def home():
    return {
        "status": "alive",
        "model_loaded": model is not None,
        "usage": "Send POST request to /predict with car details",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict")
def predict_price(car: CarPredictionInput):
    if not all([model, brand_encoder, model_encoder, feature_names]):
        raise HTTPException(
            status_code=500,
            detail="Model or encoders not loaded. Run training_model.py first."
        )

    try:
        # Encode brand and model
        try:
            brand_encoded = brand_encoder.transform([car.brand])[0]
        except ValueError:
            # If brand is unknown, use a default value
            brand_encoded = -1

        try:
            model_encoded = model_encoder.transform([car.model])[0]
        except ValueError:
            # If model is unknown, use a default value
            model_encoded = -1

        # Encode transmission (Manuelle = 0, Automatique = 1)
        transmission_encoded = 1 if car.transmission == "Automatique" else 0

        # Calculate age from year (model was trained on age, not actual year)
        age = 2025 - car.year

        # Encode fuel type (Essence = 0, Diesel = 1, Hybrid = 2)
        fuel_mapping = {"Essence": 0, "Diesel": 1, "Hybrid": 2}
        fuel_encoded = fuel_mapping.get(car.fuel_type, 0)

        # Create DataFrame with the same feature order as training
        input_data = {
            'year': age,
            'mileage': car.mileage,
            'cv': car.cv,
            'fuel_type': fuel_encoded,
            'transmission': transmission_encoded,
            'brand_encoded': brand_encoded,
            'model_encoded': model_encoded
        }

        # Reorder to match feature_names
        input_df = pd.DataFrame([input_data])[feature_names]

        # Make prediction
        prediction = model.predict(input_df)[0]

        return {
            "input": car,
            "estimated_price_tnd": int(max(0, prediction)),  # Ensure non-negative price
            "message": "Prediction successful",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

# To run: 
# pip install fastapi uvicorn scikit-learn pandas beautifulsoup4 requests
# python training_model.py  (to train and save model)
# uvicorn backend:app --reload