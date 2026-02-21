from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.models import AdminUser
from app.auth.schemas import AdminUserCreate, AdminUserResponse, Token
from app.auth.service import create_access_token, get_password_hash, verify_password
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: AdminUserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(AdminUser)
        .filter(
            (AdminUser.username == user_data.username)
            | (AdminUser.email == user_data.email)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    new_user = AdminUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(AdminUser)
        .filter(AdminUser.username == form_data.username)
        .first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me", response_model=AdminUserResponse)
def get_me(current_user: AdminUser = Depends(get_current_user)):
    return current_user
