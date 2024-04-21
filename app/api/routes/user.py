from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependency import get_db
from app.models import schemas
from app.controllers import user_controller
from ...controllers.auth_controller import get_current_user

router = APIRouter()

user_deps = Annotated[dict, Depends(get_current_user)]

@router.get('/',
            tags=["user"],
            response_model=list[schemas.User],
)
async def get_users(
        user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    db_users = user_controller.get_users(db, skip=skip, limit=limit)
    if db_users is None:
        raise HTTPException(
            status_code=200,
            detail="No users found",
        )
    return db_users

@router.post('/', tags=["user"], response_model=schemas.User)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
        userLogin: schemas.User = Depends(get_current_user),
):
    user_email = user_controller.get_user_by_email(db, user.email)
    user_username = user_controller.get_user_by_username(db, user.username)
    if user_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    if user_username:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    return user_controller.create_user(db=db, user=user)

@router.get('/{user_id}', tags=["user"], response_model=schemas.User)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(get_current_user),
):
    db_user = user_controller.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return db_user

@router.put('/{user_id}/update', tags=["user"], response_model=schemas.User)
def update_user(
        user_id: int,
        user: schemas.UserUpdate,
        db: Session = Depends(get_db),
        userLogin: schemas.User = Depends(get_current_user),
):
    return user_controller.update_user(db=db, user=user, user_id=user_id)

@router.delete('/{user_id}/delete', tags=["user"], status_code=204)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        user: schemas.User = Depends(get_current_user),
):
    return user_controller.delete_user(db, user_id=user_id)