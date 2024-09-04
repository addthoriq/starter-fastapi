from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from app.models.userModel import User
from ..migrations.database_migrations import Post
from ..models import postModel

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Post)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_my_posts(db: Session, current_user: User):
    return (
        db.query(Post)
        .where(Post.user_id == current_user.id)
    )

def get_my_post(db: Session, current_user: User, post_id: int):
    return (
        db.query(Post)
        .filter(Post.user_id == current_user.id, Post.id == post_id)
    )

def store_post(db: Session, post: postModel.PostCreate, current_user: User):
    db_post = Post(
        **post.dict(),
        user_id=current_user.id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post: postModel.PostUpdate, current_user: User, post_id: int):
    my_post = get_my_post(db, current_user, post_id).first()
    if my_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.execute(
        update(Post)
        .where(Post.id == post_id)
        .where(Post.user_id == current_user.id)
        .values(**post.dict(), user_id=current_user.id)
    )
    my_post.title = post.title
    my_post.description = post.description
    my_post.user_id = current_user.id
    db.commit()
    return my_post

def delete_post(db: Session, post_id: int, current_user: User):
    my_post = get_my_post(db, current_user, post_id)
    if my_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.execute(
        delete(Post)
        .where(Post.id == post_id)
        .where(Post.user_id == current_user.id)
    )
    db.commit()
