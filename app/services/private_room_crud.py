from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.private_chat_rooms import PrivateRoom
from app.models.users import User
from app.schemas.private_room import CreatePrivateRoom


async def create_private_room(
    user_id: CreatePrivateRoom,
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    print("user.id --->", user.id, user_id.user_id)
    new_room = PrivateRoom(
        user_id1=user.id,
        user_id2=user_id.user_id,
    )

    db.add(new_room)

    # handles commiting data to db and rollback in case of error
    try:
        await db.commit()
        await db.refresh(new_room)
    except Exception as e:
        await db.rollback()
        print("error --->", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to create private chat",
        )
    return new_room
