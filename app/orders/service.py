from sqlalchemy.orm import Session

from app.orders.models import Order, OrderDetail
from app.orders.schemas import OrderCreate, OrderUpdate, OrderDetailCreate, OrderDetailUpdate


# ── Helper ────────────────────────────────────────────────────────────

def _recalculate_order_total(db: Session, order: Order) -> None:
    """Recalculate total_amount from the sum of all detail total_prices."""
    total = sum(float(d.total_price) for d in order.details)
    order.total_amount = total
    db.flush()


# ── Order CRUD ────────────────────────────────────────────────────────

def create_order(db: Session, order_data: OrderCreate) -> Order:
    order = Order(
        order_number=order_data.order_number,
        user_id=order_data.user_id,
        source_website=order_data.source_website,
        status=order_data.status,
        total_amount=0.00,
    )
    db.add(order)
    db.flush()  # flush to get order.id

    total_amount = 0.00
    for detail_data in order_data.details:
        total_price = detail_data.quantity * detail_data.unit_price
        detail = OrderDetail(
            order_id=order.id,
            product_id=detail_data.product_id,
            quantity=detail_data.quantity,
            unit_price=detail_data.unit_price,
            total_price=total_price,
        )
        db.add(detail)
        total_amount += total_price

    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    return order


def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    source_website: str | None = None,
    status: str | None = None,
) -> list[Order]:
    query = db.query(Order)
    if source_website:
        query = query.filter(Order.source_website == source_website)
    if status:
        query = query.filter(Order.status == status)
    return query.offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def update_order(db: Session, order_id: int, order_data: OrderUpdate) -> Order | None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    update_fields = order_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> Order | None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return order


# ── Order Detail CRUD ─────────────────────────────────────────────────

def add_order_detail(
    db: Session, order_id: int, detail_data: OrderDetailCreate
) -> OrderDetail | None:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    total_price = detail_data.quantity * detail_data.unit_price
    detail = OrderDetail(
        order_id=order_id,
        product_id=detail_data.product_id,
        quantity=detail_data.quantity,
        unit_price=detail_data.unit_price,
        total_price=total_price,
    )
    db.add(detail)
    db.flush()

    _recalculate_order_total(db, order)
    db.commit()
    db.refresh(detail)
    return detail


def update_order_detail(
    db: Session, detail_id: int, detail_data: OrderDetailUpdate
) -> OrderDetail | None:
    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()
    if not detail:
        return None

    update_fields = detail_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(detail, field, value)

    # Recalculate the detail total_price
    detail.total_price = detail.quantity * float(detail.unit_price)
    db.flush()

    # Recalculate the parent order total_amount
    order = db.query(Order).filter(Order.id == detail.order_id).first()
    if order:
        _recalculate_order_total(db, order)

    db.commit()
    db.refresh(detail)
    return detail


def delete_order_detail(db: Session, detail_id: int) -> OrderDetail | None:
    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()
    if not detail:
        return None

    order_id = detail.order_id
    db.delete(detail)
    db.flush()

    # Recalculate the parent order total_amount
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        _recalculate_order_total(db, order)

    db.commit()
    return detail
