from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.core.database import get_session
from app.models.users import User

oauth2_scheme = OAuth2PasswordBearer("/auth/login")

# if any errors occur with token creation then look at expire


# creates jwt token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("user_id")
        if not user_id:
            raise credentials_exception

        # Ensure the id is a valid UUID for downstream DB lookups
        token_data = uuid.UUID(user_id)
    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_exception
    return token_data


# this is used to verify the logged in user for performing path operations that auth protected
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user_check = await db.get(User, token_data)
    if user_check is None:
        raise credentials_exception
    return user_check
