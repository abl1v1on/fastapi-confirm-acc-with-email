from fastapi import HTTPException, status

from .schemas import JWTType


class InvalidCredentialsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )


class TokenHasExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token has expired",
        )


class TokenDecodeException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token decode error",
        )


class InvalidTokenTypeException(HTTPException):
    def __init__(self, token_type: JWTType = JWTType.ACCESS) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"token type must be {token_type.value}",
        )
