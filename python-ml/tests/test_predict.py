import numpy as np
import pytest
from fastapi.testclient import TestClient
from app import app
from routes import predict as predict_module

# Define a dummy model with predictable outputs
class DummyModel:
    def predict(self, features):
        # Always return 1 as the prediction
        return [1]

    def predict_proba(self, features):
        # Return a dummy probability distribution; assume a binary classifier
        return [[0.1, 0.9]]

# Use a pytest fixture to override the model in the predict module
@pytest.fixture(autouse=True)
def override_model(monkeypatch):
    monkeypatch.setattr(predict_module, "model", DummyModel())

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict():
    # Provide a sample payload (adjust the number of features as needed)
    payload = {"features": [5.1, 3.5, 1.4, 0.2]}
    response = client.post("/predict", json=payload)
    
    # Verify that the status code is OK
    assert response.status_code == 200

    data = response.json()
    
    # Check that the response has the expected keys and values
    assert "prediction" in data
    assert "probability" in data

    # With our DummyModel, we expect a prediction of 1 and probability of 0.9
    assert data["prediction"] == 1
    # Allow a small margin for floating-point differences
    assert abs(data["probability"] - 0.9) < 0.01
