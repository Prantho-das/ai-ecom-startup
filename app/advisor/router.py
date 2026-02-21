from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.advisor.schemas import AdvisorRequest, AdvisorResponse
from app.advisor.service import AdvisorService

router = APIRouter(
    prefix="/advisor",
    tags=["AI Merchant Advisor"]
)

@router.post("/ask", response_model=AdvisorResponse)
def ask_merchant_advisor(request: AdvisorRequest, db: Session = Depends(get_db)):
    """
    Ask high-level business questions to the AI Merchant Advisor.
    Example: "Which district has the highest sales?" or "Should I invest more in Panjabi?"
    """
    answer = AdvisorService.ask_advisor(db, request.query)
    return {
        "answer": answer,
        "generated_at": datetime.now()
    }
