
# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://ml_service:8001/predict")

app = FastAPI(title="Digital Body Language - Backend")

class InteractionPayload(BaseModel):
    user_id: str
    session_id: str
    typing_speed_chars_per_sec: float
    avg_pause_ms: float
    backspace_rate: float
    scroll_depth_pct: float
    click_rate_per_min: float
    timestamp: float

@app.post("/v1/interaction")
def receive_interaction(payload: InteractionPayload):
    # Basic validation
    data = payload.dict()
    try:
        r = requests.post(ML_SERVICE_URL, json=data, timeout=5)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"ML service unavailable: {e}")

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="ML service error")

    resp = r.json()
    # persist or return result
    return {"status": "ok", "score": resp.get("score"), "label": resp.get("label"), "details": resp.get("details")}
