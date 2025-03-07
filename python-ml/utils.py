import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_request(features, prediction, confidence):
    """Logs model input and output in a structured format."""
    log_data = json.dumps({
        "features": features.tolist(),
        "prediction": prediction,
        "confidence": confidence
    })
    logging.info(log_data)

