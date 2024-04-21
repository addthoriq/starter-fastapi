from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..api.dependency import get_db
from ..migrations import database_migrations as schemes

from ..models.tokenModel import TokenData
from .user_controller import get_user_by_username

SECRET_KEY = "442cf0cfbe58d7231f1d9d6f5ba3ebe84649724cdb4084258877b4c0e2b3eb4d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username:str, password:str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

async def get_current_user(
        db: Annotated[Session, Depends(get_db)],
        token: Annotated[
            str,
            Depends(oauth2_scheme)
        ]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


def change_password(db: Session, old_password: str, new_password: str, current_user: schemes.User):
    user = get_user_by_username(db, username=current_user.username)
    if not verify_password(old_password, user.hashed_password):
        return False
    if old_password == new_password:
        return False
    user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return user