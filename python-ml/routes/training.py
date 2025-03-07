import threading
from fastapi import APIRouter

router = APIRouter()
@router.post("/retrain")
async def retrain():
    def train():
        import train_model  # Import your training script
        train_model.run_training()  # Function inside train_model.py
        
    threading.Thread(target=train).start()  # Run training asynchronously

    return {"message": "Model retraining started"}
