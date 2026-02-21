from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    product_name: str
    barcode: str | None = None
    price: Decimal
    sku: str
    variant: str | None = None
    source_website: str


class ProductUpdate(BaseModel):
    product_name: str | None = None
    barcode: str | None = None
    price: Decimal | None = None
    sku: str | None = None
    variant: str | None = None
    source_website: str | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    barcode: str | None
    price: Decimal
    sku: str
    variant: str | None
    source_website: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
