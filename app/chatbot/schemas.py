from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    product_id: Optional[int] = None # If asking about a specific product

class ChatResponse(BaseModel):
    reply: str
    source: str # 'ai' or 'knowledge_base'
