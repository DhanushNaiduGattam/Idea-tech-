from fastapi import FastAPI
from pydantic import BaseModel
import joblib, numpy as np

app = FastAPI()
model = joblib.load("outbreak_model.joblib")

class PredictRequest(BaseModel):
    village: str
    symptoms: list = []
    cases: int = 0
    turbidity: float = None
    bacterial_index: float = None
    season: int = 0

@app.post("/predict")
def predict(req: PredictRequest):
    turb = req.turbidity if req.turbidity is not None else 1.0
    bact = req.bacterial_index if req.bacterial_index is not None else 0.1
    X = np.array([[req.cases, turb, bact, req.season]])
    prob = model.predict_proba(X)[0,1]
    risk = "high" if prob > 0.5 else "low"
    return {"village": req.village, "score": float(prob), "risk": risk}