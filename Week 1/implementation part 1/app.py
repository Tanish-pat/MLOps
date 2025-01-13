from fastapi import FastAPI
from pydantic import BaseModel
from model_predictor import ModelPredictor

app = FastAPI()
predictor = ModelPredictor()

# Define the request body schema
class MessageRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Spam detection API"}

@app.post("/predict")
def predict(request: MessageRequest):
    prediction = predictor.predict(request.message)
    return {"prediction": prediction}
