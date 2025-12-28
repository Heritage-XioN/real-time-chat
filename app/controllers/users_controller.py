from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.users import User
from app.schemas.users import UserChatResponse, UserResponse, UserUpdate
from app.services.user_crud import (
    get_logged_in_user,
    get_user_chats,
    get_users,
    update_user,
)

router = APIRouter(prefix="/users", tags=["user"])


# handles getting the logged in user
@router.get("/logged_in", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return await get_logged_in_user(user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await get_users(db)


@router.get("/chats", status_code=status.HTTP_200_OK, response_model=UserChatResponse)
async def chats(
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await get_user_chats(db, user)


@router.patch("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user_details(
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await update_user(user_data, db, user)
