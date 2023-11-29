from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db_and_models.models import UserModel, User
from app.db_and_models.session import get_session
from app.crud.users import create_user, login_user
from app.auth.auth import get_current_user


router = APIRouter(tags=["Users"])

@router.post("/users", status_code=201)
async def create_user_endpoint(usermodel: UserModel, db: Session = Depends(get_session)):
    return await create_user(usermodel=usermodel, db=db)


@router.get("/users/me/", status_code=200)
async def read_user_endpoint_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/login", status_code=200)
async def login_user_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    return await login_user(form_data=form_data, db=db)