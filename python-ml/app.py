from fastapi import FastAPI
from routes import health, predict, training

app = FastAPI()

# Include routes
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(training.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)