import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr
    username: str
