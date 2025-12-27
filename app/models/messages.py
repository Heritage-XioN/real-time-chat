import uuid

from sqlalchemy import TIMESTAMP, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UUID

from app.core.database import Base


# db table for messages
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    room: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("private.id"), UUID(as_uuid=True), nullable=False
    )
    sender: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    def __repr__(self):
        return f"<Message(id={self.id}, room='{self.room}', sender='{self.sender}', content='{self.content}', timestamp='{self.timestamp}')>"
