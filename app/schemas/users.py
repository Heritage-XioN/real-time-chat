import uuid
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.private_room import PrivateRoomBase


class UserBase(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    pass


class UserChatResponse(UserBase):
    rooms_as_user1: List[PrivateRoomBase]
    pass


class UserUpdate(BaseModel):
    email: EmailStr
    username: str
