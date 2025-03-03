from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
