from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import user as user_schemas
from app.utils.security import verify_password, get_password_hash
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

def create_user(user: user_schemas.UserCreate, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def change_user_password(password_data: user_schemas.ChangePassword, db: Session):
    user = authenticate_user(password_data.email, password_data.old_password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password incorrect")
    user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"msg": "Password changed successfully"}

def reset_password_request(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Logic for sending reset password email (can implement later)
    return {"msg": "Password reset email sent"}
