from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.insights.service import InsightService
from app.insights.schemas import InsightResponse, InsightBase

router = APIRouter(
    prefix="/insights",
    tags=["AI Insights"]
)

@router.get("/", response_model=InsightResponse)
def get_ai_insights(db: Session = Depends(get_db)):
    """
    Get all AI generated insights for the merchant.
    Includes Smart Ad Target, Pricing Signals, Sourcing Guide, and Personalized Offers.
    """
    try:
        insights = InsightService.get_all_insights(db)
        return {
            "insights": insights,
            "generated_at": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/marketing", response_model=List[InsightBase])
def get_marketing_insights(db: Session = Depends(get_db)):
    return InsightService.get_ad_target_insights(db)

@router.get("/pricing", response_model=List[InsightBase])
def get_pricing_signals(db: Session = Depends(get_db)):
    return InsightService.get_pricing_signals(db)
