from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StockAlert(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    predicted_stock_out_days: int
    action_required: str # 'Order Now', 'Monitor', 'Excess'

class DeadStockReport(BaseModel):
    product_id: int
    product_name: str
    days_since_last_sale: int
    suggestion: str

class InventorySummary(BaseModel):
    low_stock_items: List[StockAlert]
    dead_stock_items: List[DeadStockReport]
    generated_at: datetime
