from pydantic import BaseModel

class InteractionPayload(BaseModel):
    user_id: str
    session_id: str
    typing_speed_chars_per_sec: float
    avg_pause_ms: float
    backspace_rate: float
    scroll_depth_pct: float
    click_rate_per_min: float
    timestamp: float

