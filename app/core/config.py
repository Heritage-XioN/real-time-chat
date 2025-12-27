from pydantic_settings import BaseSettings, SettingsConfigDict

# sets up config for accessing env variables
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_HOSTNAME: str = ""
    DB_PORT: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    TEST_DB_NAME: str = ""
    DB_DRIVER: str = ""
    DB_USERNAME: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3
    BACKEND_URL: str = ""


settings = Settings()
