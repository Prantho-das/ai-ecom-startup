from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdvisorRequest(BaseModel):
    query: str

class AdvisorResponse(BaseModel):
    answer: str
    data_points: Optional[dict] = None # Optional raw data if needed for UI
    generated_at: datetime
