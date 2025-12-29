import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.users import User


# db table for private_chat
class PrivateRoom(Base):
    __tablename__ = "private"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id1: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_id2: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    initiated_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    # RELATIONSHIPS
    user1: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id1], back_populates="rooms_as_user1"
    )

    user2: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id2], back_populates="rooms_as_user2"
    )

    __table_args__ = (
        # Enforces that each user pair can only have one private room
        UniqueConstraint("user_id1", "user_id2", name="unique_user_pair"),
        # This prevents ('userB', 'userA') from being inserted if ('userA', 'userB') already exists
        CheckConstraint("user_id1 < user_id2", name="check_user_order"),
    )
