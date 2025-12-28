from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.users import User


async def get_logged_in_user(user: Annotated[User, Depends(get_current_user)]):
    # returns a error if user is not logged in
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "user not authenticated")
    return user
