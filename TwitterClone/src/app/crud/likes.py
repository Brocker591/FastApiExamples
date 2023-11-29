from sqlmodel import Session, select
from fastapi import HTTPException

from app.db_and_models.models import LikeModel, Like, Post, User


async def create_like(like: LikeModel, db: Session, user_id: int):
    user = db.exec(select(User).where(User.id == user_id)).first()
    post = db.exec(select(Post).where(Post.id == like.post_id)).first()

    if not user or not post:
        raise HTTPException(status_code=404, detail="User or post not found")

    existing_like = db.exec(
        select(Like).where(Like.user_id == user_id).where(Like.post_id == like.post_id)
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="User as already like this post")

    like = Like(user_id=user_id, post_id=like.post_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return {"success": "Like added "}

async def delete_like(like_id: int, db: Session, user_id: int):
    like = db.exec(select(Like).where(Like.id == like_id)).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    if like.user_id != user_id:
        raise HTTPException(status_code=401, detail="Not authorized")

    db.delete(like)
    db.commit()
    return { "success":"like remove"}


async def get_like_of_post(post_id: int, db: Session):
    post = db.exec(select(Post).where(Post.id == post_id)).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    likes = db.exec(select(Like).where(Like.post_id == post_id)).all()
    return likes