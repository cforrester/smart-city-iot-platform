from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import numpy as np
import joblib  # For loading the model
import logging

# Initialize the router
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the input data schema
class InputData(BaseModel):
    features: list[float] = Field(..., example=[5.1, 3.5, 1.4, 0.2])

# Define the response schema
class PredictionOutput(BaseModel):
    prediction: int
    probability: float

# Load the model
try:
    model = joblib.load("model.pkl")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None  # Handle missing model error properly

@router.post("/predict", response_model=PredictionOutput)
async def predict(data: InputData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    try:
        # Convert input to numpy array
        features = np.array(data.features).reshape(1, -1)
        logging.info(f"Received features: {features.tolist()}")

        # Make a prediction
        prediction = model.predict(features)[0]

        # Ensure predict_proba output is a NumPy array
        proba = np.array(model.predict_proba(features)[0])  # Convert to NumPy array
        probability = float(proba.max())  # Now .max() works correctly

        logging.info(f"Prediction: {prediction}, Probability: {probability}")

        return PredictionOutput(prediction=prediction, probability=probability)
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")
