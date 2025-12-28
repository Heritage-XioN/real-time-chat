from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.auth import LoginResponse, Signup, SignupResponse
from app.services.auth_crud import create_user, login

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=SignupResponse
)
async def signup(user: Signup, db: Annotated[AsyncSession, Depends(get_session)]):
    return await create_user(user, db)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user(
    login_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    return await login(login_credentials, db)
