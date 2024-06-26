from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db_and_models.models import FollowerModel, Follower, User
from app.db_and_models.session import get_session
from app.crud.followers import create_follower, delete_following, get_following
from app.auth.auth import get_current_user

router = APIRouter(tags=["Followers"])


@router.post("/followers", status_code=201)
async def create_follower_endpoint(follower: FollowerModel, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await create_follower(followerModel=follower, db=db, user_id=current_user.id)

@router.delete("/followers/{follower_id}", status_code=204)
async def create_follower_endpoint(follower_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await delete_following(follower_id=follower_id, db=db, user_id=current_user.id)

@router.get("/followers/{user_id}", status_code=200)
async def get_followers_endpoint(user_id: int, db: Session = Depends(get_session)):
    return await get_following(user_id=user_id, db=db)