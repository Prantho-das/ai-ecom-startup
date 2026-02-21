from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str


class AdminUserLogin(BaseModel):
    username: str
    password: str


class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: int | None = None
