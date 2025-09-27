from email.message import EmailMessage

import aiosmtplib
import jwt
import bcrypt
import secrets
from typing import Annotated
from fastapi import Depends
from datetime import datetime, timezone, timedelta
from jwt.exceptions import ExpiredSignatureError, DecodeError

from core import settings
from core.models import User, helper
from api.users.service import UserAPIService
from .schemas import (
    PayloadSchema,
    JWTType,
    AccessTokenSchema,
    AuthCredentialsSchema,
)
from . import exc


class AuthAPIService:
    def __init__(self) -> None:
        self.public_key = settings.jwt.public_key
        self.private_key = settings.jwt.private_key
        self.algorithm = settings.jwt.algorithm

    async def auth_user(
        self,
        credentials: AuthCredentialsSchema,
    ) -> AccessTokenSchema:
        async with helper.session_factory() as session:
            users_service = UserAPIService(session=session)
            user = await users_service.get_user_by(
                need_raise_exception=False,
                username=credentials.username,
            )

        if not user or not self.__verify(credentials.password, user.password):
            raise exc.InvalidCredentialsException()

        token_schema = self.get_token_schema(source=user)
        return token_schema

    async def refresh_token(self, payload: PayloadSchema) -> AccessTokenSchema:
        if payload.typ != JWTType.REFRESH:
            raise exc.InvalidTokenTypeException(JWTType.REFRESH)

        token_schema = self.get_token_schema(source=payload)
        return token_schema

    def get_token_schema(self, source: User | PayloadSchema) -> AccessTokenSchema:
        access_token = self.create_token(token_type=JWTType.ACCESS, source=source)
        refresh_token = self.create_token(token_type=JWTType.REFRESH, source=source)
        return AccessTokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def encode_jwt(self, payload: PayloadSchema) -> str:
        token = jwt.encode(
            payload=payload.model_dump(),
            key=self.private_key,
            algorithm=self.algorithm,
        )
        return token

    def decode_jwt(self, token: str) -> PayloadSchema:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.public_key,
                algorithms=[self.algorithm],
            )
        except ExpiredSignatureError:
            raise exc.TokenHasExpiredException()
        except DecodeError:
            raise exc.TokenDecodeException()
        return PayloadSchema(**payload)

    def create_token(self, token_type: JWTType, source: User | PayloadSchema):
        if isinstance(source, User):
            payload = PayloadSchema(
                sub=str(source.id),
                email=source.email,  # type: ignore
                is_activated=source.is_activated,
                typ=token_type,
                **self.__generate_iat_and_exp(token_type),
            )
        elif isinstance(source, PayloadSchema):
            payload = source.model_copy(update=self.__generate_iat_and_exp(token_type))
            payload.typ = token_type
        return self.encode_jwt(payload)

    @staticmethod
    def __verify(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )

    @staticmethod
    def __generate_iat_and_exp(token_type: JWTType) -> dict[str, datetime]:
        iat = datetime.now(timezone.utc)

        if token_type == JWTType.ACCESS:
            exp = iat + timedelta(minutes=settings.jwt.access_token_expire_minutes)
        elif token_type == JWTType.REFRESH:
            exp = iat + timedelta(days=settings.jwt.refresh_token_expire_days)
        return {"iat": iat, "exp": exp}


class EmailService:
    def __init__(self) -> None:
        self.sender = settings.email.sender
        self.env = settings.email.env

    async def send_message(self, recipient: str) -> None:
        message = self.__collect_message(recipient)
        await aiosmtplib.send(
            message,
            hostname=settings.email.host,
            port=settings.email.port,
            sender=self.sender,
            recipients=[recipient],
        )

    def __collect_message(
        self,
        recipient: str,
        subject: str = settings.email.default_subject,
    ) -> EmailMessage:
        message = EmailMessage()
        message["From"] = self.sender
        message["To"] = recipient
        message["Subject"] = subject

        confirmation_code = self.__generate_confirmation_code()

        message.set_content(settings.email.default_plain_text)
        message.add_alternative(
            self.__generate_html_content(confirmation_code), subtype="html"
        )

        return message

    @staticmethod
    def __generate_confirmation_code() -> str:
        return str(secrets.randbelow(900000) + 100000)

    def __generate_html_content(self, confirmation_code: str):
        template = self.env.get_template("message.html")
        html_content = template.render(code=confirmation_code)
        return html_content


service_dep: type[AuthAPIService] = Annotated[
    AuthAPIService,
    Depends(AuthAPIService),
]
