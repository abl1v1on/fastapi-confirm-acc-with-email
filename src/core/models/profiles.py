from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, CheckConstraint

from .base import Base

if TYPE_CHECKING:
    from .users import User


class Profile(Base):
    first_name: Mapped[str | None] = mapped_column(String(60))
    last_name: Mapped[str | None] = mapped_column(String(60))
    bio: Mapped[str | None] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    __table_args__ = (
        CheckConstraint(
            "LENGTH(first_name) >= 1",
            name="ck_profile_first_name_len_ge_1",
        ),
        CheckConstraint(
            "LENGTH(last_name) >= 1",
            name="ck_profile_last_name_len_ge_1",
        ),
        CheckConstraint(
            "LENGTH(bio) >= 1",
            name="ck_profile_bio_len_ge_1",
        ),
    )
