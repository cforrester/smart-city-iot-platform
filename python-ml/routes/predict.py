from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import tensorflow as tf
import numpy as np
import logging
import os
import redis
import json
import time
from utils import log_request 

router = APIRouter()
logging.basicConfig(level=logging.INFO)



# Define the input data schema
class InputData(BaseModel):
    features: list[float] = Field(..., example=[5.1, 3.5, 1.4, 0.2])

# Define the response schema
class PredictionOutput(BaseModel):
    prediction: int
    confidence: float

# Load the TensorFlow model
try:
    model_dir = "models"
    if not os.path.exists(model_dir) or not os.listdir(model_dir):
        raise ValueError("No model versions found in 'models/' directory.")
    latest_version = sorted(os.listdir(model_dir))[-1]
    model_path = os.path.join(model_dir, latest_version, "model.keras")

    model = tf.keras.models.load_model(model_path)
    logging.info("TensorFlow model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None  # Handle missing model case


@router.get("/model-info")
async def model_info():
    return {"version": latest_version, "model_path": model_path}


redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@router.post("/predict", response_model=PredictionOutput)
async def predict(data: InputData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    try:
        cache_key = json.dumps(data.features)

        # Check Redis cache
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Run inference
        features = np.array(data.features).reshape(1, -1)
        predictions = model.predict(features)
        predicted_class = int(np.argmax(predictions, axis=1)[0])
        confidence = float(np.max(predictions))
        cache_prediction(features, predicted_class, confidence)
        
        return PredictionOutput(prediction=predicted_class, confidence=confidence)
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")

class BatchInput(BaseModel):
    features: list[list[float]]  # List of feature arrays

@router.post("/batch-predict")
async def batch_predict(data: BatchInput):
    features = np.array(data.features)
    predictions = model.predict(features)
    
    results = [
        {"prediction": int(np.argmax(p)), "confidence": float(np.max(p))}
        for p in predictions
    ]
    return {"results": results}

def connect_redis():
    for i in range(5):  # Retry up to 5 times
        try:
            return redis.Redis(host="redis", port=6379, decode_responses=True, socket_timeout=5)
        except redis.ConnectionError:
            logging.warning(f"Redis connection failed. Retrying {i+1}/5...")
            time.sleep(2)
    raise Exception("Redis connection failed after multiple attempts.")

# Establish Redis connection
try:
    redis_client = connect_redis()
    logging.info("Connected to Redis successfully!")
except Exception as e:
    logging.error(f"Redis Error: {e}")
    redis_client = None  # Prevents crashes if Redis is unavailable


def cache_prediction(features, prediction, confidence):
    if redis_client:
        """Caches predictions in Redis"""
        cache_key = json.dumps(features.tolist())  
        response = {
            "prediction": int(prediction),  
            "confidence": float(confidence)  
        }
        redis_client.setex(cache_key, 3600, json.dumps(response))  # Cache for 1 hour