import os
import requests

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://ml_service:8001/predict")

def send_to_ml(payload: dict):
    try:
        r = requests.post(ML_SERVICE_URL, json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error contacting ML service:", e)
        return None

