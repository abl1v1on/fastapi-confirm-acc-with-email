from fastapi import Depends
from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from core import settings


class DBHelper:
    def __init__(self) -> None:
        self.engine = create_async_engine(url=settings.db.url, echo=settings.db.echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=True, expire_on_commit=False
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


helper = DBHelper()
session_dep: type[AsyncSession] = Annotated[
    AsyncSession, Depends(helper.session_dependency)
]
