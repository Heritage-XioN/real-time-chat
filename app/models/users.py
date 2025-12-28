import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import TIMESTAMP, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.private_chat_rooms import PrivateRoom


# db table for users
class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # REVERSE RELATIONSHIPS
    # We must specify which foreign key on the PrivateRoom refers to this list
    rooms_as_user1: Mapped[List["PrivateRoom"]] = relationship(
        "PrivateRoom", back_populates="user1", foreign_keys="[PrivateRoom.user_id1]"
    )

    rooms_as_user2: Mapped[List["PrivateRoom"]] = relationship(
        "PrivateRoom", back_populates="user2", foreign_keys="[PrivateRoom.user_id2]"
    )
