
# ml_service/inference.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

app = FastAPI(title="Digital Body Language - ML Service")

class Interaction(BaseModel):
    user_id: str
    session_id: str
    typing_speed_chars_per_sec: float
    avg_pause_ms: float
    backspace_rate: float
    scroll_depth_pct: float
    click_rate_per_min: float
    timestamp: float

def load_model(path):
    try:
        return joblib.load(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

model = load_model(MODEL_PATH)

@app.post("/predict")
def predict(payload: Interaction):
    X = np.array([[
        payload.typing_speed_chars_per_sec,
        payload.avg_pause_ms,
        payload.backspace_rate,
        payload.scroll_depth_pct,
        payload.click_rate_per_min
    ]])
    prob = model.predict_proba(X)[0,1]  # probability of "engaged/positive"
    score = float(prob*100)
    label = "High Engagement" if score >= 60 else ("Medium" if score >= 35 else "Low Engagement")
    details = {
        "probability": prob,
        "features": {
            "typing_speed": payload.typing_speed_chars_per_sec,
            "avg_pause_ms": payload.avg_pause_ms,
            "backspace_rate": payload.backspace_rate,
            "scroll_depth_pct": payload.scroll_depth_pct,
            "click_rate": payload.click_rate_per_min
        }
    }
    return {"score": score, "label": label, "details": details}
