from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependency import get_db
from app.models import userModel
from app.controllers import user_controller
from ...controllers.auth_controller import get_current_user

router = APIRouter()

@router.get('/',
            tags=["user"],
            response_model=list[userModel.User],
)
async def get_users(
        user: userModel.User = Depends(get_current_user),
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

@router.post('/', tags=["user"], response_model=userModel.User)
def create_user(
        user: userModel.UserCreate,
        db: Session = Depends(get_db),
        userLogin: userModel.User = Depends(get_current_user),
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

@router.get('/{user_id}', tags=["user"], response_model=userModel.User)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        user: userModel.User = Depends(get_current_user),
):
    db_user = user_controller.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return db_user

@router.put('/{user_id}/update', tags=["user"], response_model=userModel.User)
def update_user(
        user_id: int,
        user: userModel.UserUpdate,
        db: Session = Depends(get_db),
        userLogin: userModel.User = Depends(get_current_user),
):
    return user_controller.update_user(db=db, user=user, user_id=user_id)

@router.delete('/{user_id}/delete', tags=["user"], status_code=204)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        user: userModel.User = Depends(get_current_user),
):
    return user_controller.delete_user(db, user_id=user_id)