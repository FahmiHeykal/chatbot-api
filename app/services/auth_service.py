from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import TokenData

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)

def get_password_hash(password: str) -> str:
    return pwd_ctx.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    print("DEBUG: token diterima:", token)  # Debug log

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("DEBUG: payload hasil decode:", payload)  # Debug log

        username = payload.get("sub")
        is_admin = payload.get("is_admin", False)

        if not username:
            print("DEBUG: username tidak ditemukan di payload")
            raise credentials_error

    except JWTError as e:
        print("DEBUG: JWT decode error:", e)
        raise credentials_error

    user = get_user(db, username=username)
    print("DEBUG: hasil get_user:", user)  # Debug log

    if not user:
        print("DEBUG: user tidak ditemukan di database")
        raise credentials_error

    return user
    
async def get_current_active_user(user: Annotated[User, Depends(get_current_user)]):
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

async def get_admin_user(user: Annotated[User, Depends(get_current_user)]):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient privileges")
    return user
