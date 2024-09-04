from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependency import get_db
from app.models import postModel, userModel
from app.controllers import post_controller
from ...controllers.auth_controller import get_current_user

router = APIRouter()

@router.get('/', tags=['post'], response_model=list[postModel.Post])
async def get_posts(
        db: Session = Depends(get_db),
        user: userModel = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100,
):
    db_posts = post_controller.get_posts(db, skip, limit)
    return db_posts

@router.get('/my-posts',
            tags=['post'],
            response_model=list[postModel.Post])
def get_my_posts(
        db: Session = Depends(get_db),
        user: userModel.User = Depends(get_current_user),
):
    db_posts = post_controller.get_my_posts(db, user)
    if db_posts is None:
        raise HTTPException(
            status_code=204,
            detail="No posts found",
        )
    return db_posts

@router.post('/store-post', tags=['post'], response_model=postModel.Post)
def store_post(
        post: postModel.PostCreate,
        db: Session = Depends(get_db),
        user: userModel.User = Depends(get_current_user),
):
    return post_controller.store_post(db, post, user)

@router.put('/{post_id}/my-post', tags=['post'], response_model=postModel.Post)
def update_post(
        post: postModel.PostUpdate,
        post_id: int,
        db: Session = Depends(get_db),
        user: userModel.User = Depends(get_current_user),
):
    return post_controller.update_post(db, post, user, post_id)

@router.delete('/{post_id}/delete', tags=["post"], status_code=204)
def delete_user(
        post_id: int,
        db: Session = Depends(get_db),
        user: userModel.User = Depends(get_current_user),
):
    return post_controller.delete_post(db, post_id, user)
