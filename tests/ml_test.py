# tests/ml_test.py
import joblib
import numpy as np
import os
def test_model_exists():
    assert os.path.exists("ml_service/model.pkl")
def test_model_predict():
    model = joblib.load("ml_service/model.pkl")
    X = np.array([[5.0, 100.0, 0.05, 70.0, 10.0]])
    probs = model.predict_proba(X)
    assert probs.shape == (1,2)

