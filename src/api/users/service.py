import bcrypt
from fastapi import Depends
from typing import Sequence, Annotated
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core import BaseAPIService
from core.models import User, Profile
from .schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    PartialUpdateUserSchema,
)
from . import exc


class UserAPIService(BaseAPIService):
    async def get_users(self) -> Sequence[User]:
        stmt = select(User).order_by(User.id.desc())
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        return users

    async def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise exc.UserNotFoundException()
        return user

    async def create_user(self, schema: CreateUserSchema) -> User:
        schema.password = self.__hash_password(schema.password)
        new_user = User(**schema.model_dump())
        new_profile = Profile()

        try:
            async with self.session.begin():
                self.session.add(new_user)
                await self.session.flush()

                new_profile.user_id = new_user.id
                self.session.add(new_profile)

        except IntegrityError as e:
            err_msg = str(e.orig)

            if "uq_user_username" in err_msg:
                raise exc.UsernameIsBusyException()
            elif "uq_user_email" in err_msg:
                raise exc.EmailIsBusyException()

        return new_user

    async def update_user(
        self,
        user_id: int,
        schema: UpdateUserSchema | PartialUpdateUserSchema,
    ) -> User:
        user = await self.get_user_by_id(user_id)
        is_partial = isinstance(schema, PartialUpdateUserSchema)

        for key, value in schema.model_dump(exclude_none=is_partial).items():
            setattr(user, key, value)

        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()

            err_msg = str(e.orig)

            if "uq_user_username" in err_msg:
                raise exc.UsernameIsBusyException()
            elif "uq_user_email" in err_msg:
                raise exc.EmailIsBusyException()
        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        await self.session.delete(user)
        await self.session.commit()

    @staticmethod
    def __hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=password.encode(), salt=salt)
        return hashed.decode()


service_dep: type[UserAPIService] = Annotated[
    UserAPIService, Depends(UserAPIService.get_service)
]
