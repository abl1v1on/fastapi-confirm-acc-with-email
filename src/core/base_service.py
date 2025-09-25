from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import session_dep


class BaseAPIService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @classmethod
    def get_service(cls, session: session_dep) -> Self:
        return cls(session=session)
