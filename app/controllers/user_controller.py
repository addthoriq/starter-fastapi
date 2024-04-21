from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from ..models import schemas as models
from ..migrations import database_migrations as schemes

def get_user(db: Session, user_id: int):
    return (
        db.query(schemes.User)
        .filter(schemes.User.id == user_id)
        .first()
    )

def get_user_by_email(db: Session, email: str):
    return (
        db.query(schemes.User)
        .filter(schemes.User.email == email)
        .first()
    )

def get_user_by_username(db: Session, username: str):
    return (
        db.query(schemes.User)
        .filter(schemes.User.username == username)
        .first()
    )

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemes.User).offset(skip).limit(limit).all()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def create_user(db: Session, user: models.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = schemes.User(
        email=user.email,
        hashed_password=hashed_password,
        username=user.username,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: models.UserUpdate, user_id: int):
    hashed_password = pwd_context.hash(user.password)
    db_user = get_user(db, user_id)
    db_user.email=user.email,
    db_user.hashed_password=hashed_password,
    db_user.username=user.username,
    db_user.name=user.name
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(
        db: Session,
        user_id: int
):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()