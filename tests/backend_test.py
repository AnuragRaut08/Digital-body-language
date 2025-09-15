import requests
def test_backend_predict_local():
    payload = {
        "user_id": "t",
        "session_id": "s",
        "typing_speed_chars_per_sec": 4.5,
        "avg_pause_ms": 120.0,
        "backspace_rate": 0.02,
        "scroll_depth_pct": 80.0,
        "click_rate_per_min": 12.0,
        "timestamp": 1234567890
    }
    r = requests.post("http://localhost:8000/v1/interaction", json=payload, timeout=5)
    assert r.status_code == 200
    j = r.json()
    assert "score" in j

