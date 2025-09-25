from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    CheckConstraint,
    UniqueConstraint,
    DateTime,
    func,
)

from .base import Base

if TYPE_CHECKING:
    from .profiles import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(60), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    profile: Mapped["Profile"] = relationship(back_populates="user")

    __table_args__ = (
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint("email", name="uq_user_email"),
        CheckConstraint(
            "LENGTH(username) >= 3",
            name="ck_user_username_len_ge_3",
        ),
        CheckConstraint(
            "LENGTH(email) >= 6",
            name="ck_user_email_len_ge_6",
        ),
    )
