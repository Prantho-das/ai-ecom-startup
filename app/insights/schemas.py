from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class InsightBase(BaseModel):
    title: str
    message: str
    category: str  # 'marketing', 'sourcing', 'pricing', 'offer'
    priority: str  # 'high', 'medium', 'low'

class RegionalDemandInsight(InsightBase):
    region: str
    product_name: str
    growth_rate: float

class PricingSignalInsight(InsightBase):
    product_id: int
    current_price: float
    suggested_price: float
    reason: str

class SourcingInsight(InsightBase):
    item_category: str
    expected_demand_growth: str
    timeframe: str

class InsightResponse(BaseModel):
    insights: List[InsightBase]
    generated_at: datetime
