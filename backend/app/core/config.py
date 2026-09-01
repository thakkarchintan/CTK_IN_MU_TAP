from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "V1 Trading Platform"
    environment: str = "development"

    # Database
    database_url: str = "postgresql+psycopg2://trading:trading@db:5432/trading"

    # Auth
    secret_key: str = "change-me-in-env"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 12

    # Seed admin user (single-user V1 auth)
    admin_email: str = "admin@example.com"
    admin_password: str = "changeme123"

    # Display timezone (storage stays UTC; this is display-only, used by frontend/logging helpers)
    display_timezone: str = "Asia/Kolkata"

    # Zerodha Kite Connect (never exposed to frontend)
    kite_api_key: str = ""
    kite_api_secret: str = ""
    kite_access_token: str = ""


settings = Settings()
