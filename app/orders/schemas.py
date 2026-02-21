from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


# ── Order Detail Schemas ──────────────────────────────────────────────

class OrderDetailCreate(BaseModel):
    product_id: int
    quantity: int = 1
    unit_price: Decimal


class OrderDetailUpdate(BaseModel):
    quantity: int | None = None
    unit_price: Decimal | None = None


class OrderDetailResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Order Schemas ─────────────────────────────────────────────────────

class OrderCreate(BaseModel):
    order_number: str
    user_id: int
    source_website: str
    status: str = "pending"
    details: list[OrderDetailCreate] = []


class OrderUpdate(BaseModel):
    status: str | None = None
    total_amount: Decimal | None = None


class OrderResponse(BaseModel):
    id: int
    order_number: str
    user_id: int
    total_amount: Decimal
    status: str
    source_website: str
    created_at: datetime
    updated_at: datetime
    details: list[OrderDetailResponse] = []

    model_config = ConfigDict(from_attributes=True)
