from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "../models/loan_approval_model.pkl"))
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoanApplication(BaseModel):
    ApplicantIncome: float = Field(..., gt=0, description="Must be positive")
    CoapplicantIncome: float = Field(..., ge=0, description="Must be zero or positive")
    Credit_History: float = Field(..., ge=0, description="Must be zero or positive")
    LoanAmount: float = Field(..., gt=0, description="Must be positive")
    Loan_Amount_Term: float = Field(..., gt=0, description="Must be positive")
    Gender_Female: float
    Gender_Male: float
    Married_No: float
    Married_Yes: float
    Dependents_0: float
    Dependents_1: float
    Dependents_2: float
    Dependents_3_plus: float
    Education_Graduate: float
    Education_Not_Graduate: float
    Self_Employed_No: float
    Self_Employed_Yes: float
    Property_Area_Rural: float
    Property_Area_Semiurban: float
    Property_Area_Urban: float

@app.get("/")
async def home():
    return {"message": "Loan Approval Model is Running!"}

@app.post("/predict")
async def predict(data: LoanApplication):
    try:
        df = pd.DataFrame([data.dict()])
        df.rename(columns={"Dependents_3_plus": "Dependents_3+", "Education_Not_Graduate": "Education_Not Graduate"}, inplace=True)
        logger.info(f"Received input: {data.dict()}")
        prediction = model.predict(df)
        logger.info(f"Prediction: {int(prediction[0])}")
        return {"loan_approval": int(prediction[0])}

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")