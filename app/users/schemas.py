from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# ── UserAddress schemas ──────────────────────────────────────────────

class UserAddressCreate(BaseModel):
    country: str
    city: str
    district: str | None = None
    address: str


class UserAddressUpdate(BaseModel):
    country: str | None = None
    city: str | None = None
    district: str | None = None
    address: str | None = None


class UserAddressResponse(BaseModel):
    id: int
    user_id: int
    country: str
    city: str
    district: str | None
    address: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── User schemas ─────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    source_website: str


class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    source_website: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    type: str
    source_website: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    addresses: list[UserAddressResponse] = []

    model_config = ConfigDict(from_attributes=True)
