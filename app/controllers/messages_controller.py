from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.messages import Message

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/{room_name}")
async def get_messages(room_name: str, db: AsyncSession = Depends(get_session)):
    # Fetch last 50 messages
    result = await db.execute(
        select(Message)
        .where(Message.room == room_name)
        .order_by(Message.timestamp.asc())
        .limit(50)
    )
    messages = result.scalars().all()
    return messages
