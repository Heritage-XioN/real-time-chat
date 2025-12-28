from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user
from app.models.users import User
from app.schemas.users import UserUpdate


async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    # returns a error if user is not logged in
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authenticated")
    return user


async def get_users(db: Annotated[AsyncSession, Depends(get_session)]):
    user_query = await db.execute(select(User))
    result = user_query.scalars().all()
    return result


async def update_user(
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
):
    # handles getting the user object by id
    user_query = await db.get(User, user.id)

    # returns 404 not found and a message if the user does not exist
    if not user_query:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"user with the id {user.id} does not exists"
        )

    # handles updating the user in the db
    for field, value in user_data.model_dump(exclude={"id"}).items():
        setattr(user_query, field, value)

    # handles commiting data to db and rollback in case of error
    try:
        await db.commit()
        await db.refresh(user_query)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to update user data",
        )
    return user_query


# TODO: add other CRUD operations(update , delete)
