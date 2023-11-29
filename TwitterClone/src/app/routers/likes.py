from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db_and_models.models import LikeModel, Like, PostModel, Post, User
from app.db_and_models.session import get_session
from app.crud.likes import create_like, delete_like, get_like_of_post
from app.auth.auth import get_current_user

router = APIRouter(tags=["Likes"])

@router.post("/likes", status_code=201)
async def create_like_endpoint(like: LikeModel, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await create_like(like=like, db=db, user_id=current_user.id)

@router.delete("/like/{like_id}", status_code=204)
async def delete_like_endpoint(like_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await delete_like(like_id=like_id, db=db, user_id=current_user.id)


@router.get("/post/{post_id}/likes", status_code=200)
async def get_likes_endpoint(post_id: int, db: Session = Depends(get_session)):
    return await get_like_of_post(post_id=post_id, db=db)