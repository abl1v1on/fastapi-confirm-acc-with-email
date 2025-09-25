from pathlib import Path
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
    public_key: str = (BASE_DIR / "certs" / "jwt-private.pem").read_text()
    private_key: str = (BASE_DIR / "certs" / "jwt-public.pem").read_text()
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    db: DBSettings
    server: ServerSettings = ServerSettings()
    jwt: JWTSettings = JWTSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


settings = Settings()
