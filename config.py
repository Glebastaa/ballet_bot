from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_file_encoding='utf-8'
    )


class DBSettings(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MODE: str

    @property
    def DATABASE_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'


class BotSettings(EnvBaseSettings):
    bot_token: SecretStr


class Settings(DBSettings, BotSettings):
    DEBUG: bool = True


settings = Settings()
