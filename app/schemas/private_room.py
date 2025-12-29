import uuid

from pydantic import BaseModel, ConfigDict


class PrivateRoomBase(BaseModel):
    id: uuid.UUID
    user_id1: uuid.UUID
    user_id2: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class CreatePrivateRoom(BaseModel):
    user_id: uuid.UUID


class privateRoomResponse(PrivateRoomBase):
    pass
