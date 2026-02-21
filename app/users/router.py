from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.users import service
from app.users.schemas import (
    UserAddressCreate,
    UserAddressResponse,
    UserAddressUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


# ── User endpoints ───────────────────────────────────────────────────

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return service.create_user(db, user_data)


@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source_website: str | None = Query(None),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return service.get_users(db, skip=skip, limit=limit, source_website=source_website)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    user = service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    user = service.update_user(db, user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    user = service.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ── Address endpoints ────────────────────────────────────────────────

@router.post("/{user_id}/addresses", response_model=UserAddressResponse, status_code=201)
def create_address(
    user_id: int,
    address_data: UserAddressCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return service.create_user_address(db, user_id, address_data)


@router.get("/{user_id}/addresses", response_model=list[UserAddressResponse])
def list_addresses(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return service.get_user_addresses(db, user_id)


@router.put("/{user_id}/addresses/{address_id}", response_model=UserAddressResponse)
def update_address(
    user_id: int,
    address_id: int,
    address_data: UserAddressUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    address = service.update_user_address(db, address_id, address_data)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.delete("/{user_id}/addresses/{address_id}", response_model=UserAddressResponse)
def delete_address(
    user_id: int,
    address_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    address = service.delete_user_address(db, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address
