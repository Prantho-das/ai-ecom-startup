from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.orders import service
from app.orders.schemas import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderDetailCreate,
    OrderDetailUpdate,
    OrderDetailResponse,
)

router = APIRouter()


# ── Order Endpoints ───────────────────────────────────────────────────

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = service.create_order(db, order_data)
    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source_website: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    orders = service.get_orders(
        db, skip=skip, limit=limit, source_website=source_website, status=status
    )
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = service.get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = service.update_order(db, order_id, order_data)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.delete("/{order_id}", response_model=OrderResponse)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = service.delete_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


# ── Order Detail Endpoints ────────────────────────────────────────────

@router.post(
    "/{order_id}/details",
    response_model=OrderDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_order_detail(
    order_id: int,
    detail_data: OrderDetailCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    detail = service.add_order_detail(db, order_id, detail_data)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return detail


@router.get("/{order_id}/details", response_model=list[OrderDetailResponse])
def list_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    order = service.get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order.details


@router.put(
    "/{order_id}/details/{detail_id}", response_model=OrderDetailResponse
)
def update_order_detail(
    order_id: int,
    detail_id: int,
    detail_data: OrderDetailUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    detail = service.update_order_detail(db, detail_id, detail_data)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found",
        )
    return detail


@router.delete(
    "/{order_id}/details/{detail_id}", response_model=OrderDetailResponse
)
def delete_order_detail(
    order_id: int,
    detail_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    detail = service.delete_order_detail(db, detail_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found",
        )
    return detail
