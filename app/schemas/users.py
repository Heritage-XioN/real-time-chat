import uuid

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    status: str
