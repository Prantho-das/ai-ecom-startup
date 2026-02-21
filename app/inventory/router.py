from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.inventory.schemas import InventorySummary
from app.inventory.service import InventoryIntelligenceService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Intelligence"]
)

@router.get("/summary", response_model=InventorySummary)
def get_inventory_intelligence(db: Session = Depends(get_db)):
    """
    Get AI-driven inventory insights: Stock-out predictions and Dead stock alerts.
    """
    return InventoryIntelligenceService.get_inventory_summary(db)

@router.get("/low-stock")
def get_low_stock_forecast(db: Session = Depends(get_db)):
    return InventoryIntelligenceService.get_stock_out_forecast(db)
