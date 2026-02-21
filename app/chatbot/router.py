from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.chatbot.schemas import ChatRequest, ChatResponse
from app.chatbot.service import ChatbotService

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)

@router.post("/ask", response_model=ChatResponse)
def ask_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Ask any shipping or product related questions to the AI chatbot.
    """
    reply = ChatbotService.get_reply(db, request.message, request.product_id)
    return {
        "reply": reply,
        "source": "ai"
    }
