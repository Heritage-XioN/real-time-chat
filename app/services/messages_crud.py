from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.messages import Message


async def get_messages(room: str, db: Annotated[AsyncSession, Depends(get_session)]):
    # Fetch last 50 messages
    result = await db.execute(
        select(Message)
        .where(Message.room == room)
        .order_by(Message.timestamp.asc())
        .limit(50)
    )
    messages = result.scalars().all()

    # checks if there are messages in the table
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no messages yet",
        )

    return messages
