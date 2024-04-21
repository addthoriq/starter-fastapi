from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependency import get_db
from app.models import schemas
from app.controllers import user_controller

router = APIRouter()

@router.get('/',
            tags=["user"],
            response_model=list[schemas.User],
)
async def get_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    db_users = user_controller.get_users(db, skip=skip, limit=limit)
    return db_users

@router.post('/', tags=["user"], response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
):
    # db_user = user_controller.create_user(db, user)
    # if db_user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail=f"User {db_user.id} already exists",
    #     )
    return user_controller.create_user(db=db, user=user)