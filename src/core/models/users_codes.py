from sqlalchemy import ForeignKey, String, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserCode(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
    )
    code: Mapped[str] = mapped_column(String(6))

    __table_args__ = (
        CheckConstraint("LENGTH(code) = 6", name="ck_user_code_code_len_eq_6"),
        UniqueConstraint("user_id", name="uq_user_code_user_id"),
    )
