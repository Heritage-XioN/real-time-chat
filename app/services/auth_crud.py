from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import create_access_token
from app.models.users import User
from app.schemas.auth import Signup
from app.utils.helpers import hash, verify


# -- signup --
async def create_user(user: Signup, db: Annotated[AsyncSession, Depends(get_session)]):
    # query db for user
    user_query = await db.execute(select(User).where(User.email == user.email))
    result = user_query.scalars().first()

    # checks if user already exist and raise a http exception if true
    if result:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "user already exist pls login")

    # hash password
    hashed_password: str = hash(user.password)

    # Create SQLAlchemy User model from Pydantic schema
    new_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    # adds user to db if no errors
    db.add(new_user)
    await db.commit()
    return {"status": "success"}


# -- login --
async def login(
    login_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    # query db for user
    user_query = await db.execute(
        select(User).where(User.email == login_credentials.username)
    )
    result = user_query.scalars().first()

    # checks if the user exists
    if not result:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid credentials")

    # if the user exist then check if they provided the correct password
    if not verify(login_credentials.password, result.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid credentials")

    # if all statement above evaluate withot exceptions then create auth token
    access_token = create_access_token(data={"user_id": str(result.id)})
    return {"status": "success", "access_token": access_token, "token_type": "Bearer"}
