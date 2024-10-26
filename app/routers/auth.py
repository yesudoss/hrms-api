from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user as user_schemas
from app.services.auth import (
    create_user, 
    authenticate_user, 
    create_access_token, 
    change_user_password, 
    reset_password_request
)
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup")
def signup(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/change-password")
def change_password(
    password_data: user_schemas.ChangePassword,
    db: Session = Depends(get_db)
):
    return change_user_password(password_data, db)

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    return reset_password_request(email, db)
