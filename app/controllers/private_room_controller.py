from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.users import User
from app.schemas.private_room import CreatePrivateRoom, privateRoomResponse
from app.services.private_room_crud import create_private_room

router = APIRouter(prefix="/private", tags=["private room"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=privateRoomResponse,
)
async def create_room(
    user_id: CreatePrivateRoom,
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    return await create_private_room(user_id, db, user)
