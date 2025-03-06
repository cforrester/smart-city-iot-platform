from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/predict")
async def predict(data: InputData):
    # Simple simulation: randomly choose a label
    label = "positive" if random.random() > 0.5 else "negative"
    return {"prediction": {"label": label}}

# To run: uvicorn app:app --host 0.0.0.0 --port 8000
