from passlib.context import CryptContext
from jose import JWTError, jwt
from app.config import settings

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.models.user import User as UserModel
from app.config import settings
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Fetch user from DB and validate
    user = db.query(UserModel).filter(UserModel.email == user_id).first()
    if user is None:
        raise credentials_exception
    return user