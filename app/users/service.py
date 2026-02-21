from sqlalchemy.orm import Session

from app.users.models import User, UserAddress
from app.users.schemas import (
    UserAddressCreate,
    UserAddressUpdate,
    UserCreate,
    UserUpdate,
)


# ── User CRUD ────────────────────────────────────────────────────────

def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    source_website: str | None = None,
) -> list[User]:
    query = db.query(User).filter(User.is_active == True)
    if source_website is not None:
        query = query.filter(User.source_website == source_website)
    return query.offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


# ── UserAddress CRUD ─────────────────────────────────────────────────

def create_user_address(
    db: Session, user_id: int, address_data: UserAddressCreate
) -> UserAddress:
    address = UserAddress(user_id=user_id, **address_data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_user_addresses(db: Session, user_id: int) -> list[UserAddress]:
    return db.query(UserAddress).filter(UserAddress.user_id == user_id).all()


def update_user_address(
    db: Session, address_id: int, address_data: UserAddressUpdate
) -> UserAddress | None:
    address = db.query(UserAddress).filter(UserAddress.id == address_id).first()
    if address is None:
        return None
    update_data = address_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address


def delete_user_address(db: Session, address_id: int) -> UserAddress | None:
    address = db.query(UserAddress).filter(UserAddress.id == address_id).first()
    if address is None:
        return None
    db.delete(address)
    db.commit()
    return address
