import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    id: uuid.UUID
    room: uuid.UUID
    sender: str
    content: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    room: uuid.UUID
    sender: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(Message):
    pass


class GetMessagesForRoom(BaseModel):
    room: uuid.UUID
