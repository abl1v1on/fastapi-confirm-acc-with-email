from pathlib import Path

from jinja2 import FileSystemLoader, Environment
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):
    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str
    echo: bool = True

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.USER}:{self.PASS}@"
            f"{self.HOST}:{self.PORT}/"
            f"{self.NAME}"
        )


class ServerSettings(BaseModel):
    app: str = "main:app"
    reload: bool = True
    host: str = "localhost"
    port: int = 8000


class JWTSettings(BaseModel):
    public_key: str = (BASE_DIR / "certs" / "jwt-public.pem").read_text()
    private_key: str = (BASE_DIR / "certs" / "jwt-private.pem").read_text()
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10
    refresh_token_expire_days: int = 30


class EmailSettings(BaseSettings):
    sender: str = "admin@admin.com"
    host: str = "localhost"
    port: int = 1025
    env: Environment = Environment(loader=FileSystemLoader(BASE_DIR / "templates"))

    default_subject: str = "Активируйте ваш аккаунт"
    default_plain_text: str = "Ваш почтовый клиент не поддерживает HTML"


class Settings(BaseSettings):
    db: DBSettings
    server: ServerSettings = ServerSettings()
    jwt: JWTSettings = JWTSettings()
    email: EmailSettings = EmailSettings()

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, env_nested_delimiter="__"
    )


settings = Settings()
