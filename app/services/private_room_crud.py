from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.private_chat_rooms import PrivateRoom
from app.models.users import User
from app.schemas.private_room import CreatePrivateRoom


async def create_private_room(
    data: CreatePrivateRoom,
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    # check if the other user exist
    other_user = await db.get(User, data.user_id)
    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Prevent self-messaging
    if user.id == data.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot create a private chat with yourself.",
        )

    # handles sorting the user ids
    # this is necessary for the private room database constraint
    u1, u2 = sorted((user.id, data.user_id))

    new_room = PrivateRoom(
        user_id1=u1,
        user_id2=u2,
        initiated_by=user.id,
    )

    # add to db
    db.add(new_room)

    # handles commiting data to db and rollback in case of error
    try:
        await db.commit()
        await db.refresh(new_room)
    except IntegrityError:
        # catch the duplicate error gracefully
        await db.rollback()

        # return the existing room
        existing_room = await db.execute(
            select(PrivateRoom).where(
                PrivateRoom.user_id1 == u1, PrivateRoom.user_id2 == u2
            )
        )
        return existing_room.scalar_one_or_none()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failed to create private chat: {e}",
        )
    return new_room
