<<<<<<< HEAD
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
=======
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
>>>>>>> 0be1bad (Какая-то чухня)


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
<<<<<<< HEAD
=======

    bot_token: SecretStr
>>>>>>> 0be1bad (Какая-то чухня)

    @property
    def DATABASE_url_asyncpg(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'


class BotSettings(EnvBaseSettings):
    bot_token: SecretStr


<<<<<<< HEAD
class Settings(DBSettings, BotSettings):
    DEBUG: bool = True


=======
>>>>>>> 0be1bad (Какая-то чухня)
settings = Settings()
