from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Cashback Rewards Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str

    GEMINI_API_KEY: str

    # Fernet key (url-safe base64). Used for mobile encrypt/decrypt
    # and as HMAC secret for mobile_hash lookups.
    FIELD_ENCRYPTION_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()