from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.messages import MessageResponse
from app.services.messages_crud import get_messages

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get(
    "/{room}", status_code=status.HTTP_200_OK, response_model=List[MessageResponse]
)
async def messages(room: str, db: Annotated[AsyncSession, Depends(get_session)]):
    return await get_messages(room, db)
