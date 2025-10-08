"""
Application Configuration Management

This module defines the configuration for the Orion backend application.
It uses Pydantic's BaseSettings to load configuration from environment
variables and .env files, allowing for a clear and type-safe way to
manage settings.

The configuration is separated into logical groups:
- Database: Connection settings for PostgreSQL.
- JWT: Settings for JSON Web Token authentication.
- CORS: Cross-Origin Resource Sharing policies.
- AI: Optional settings for AI-powered features.
"""

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    """
    Defines the application's settings, loaded from environment variables.
    """
    
    # --- Database Configuration ---
    # The full connection string for the PostgreSQL database.
    # Example: postgresql+psycopg2://user:password@host:port/dbname
    DATABASE_URL: PostgresDsn = Field(..., description="PostgreSQL connection URL")

    # --- JWT (JSON Web Token) Configuration ---
    # The secret key used to sign and verify JWTs.
    # It is critical that this is kept secret.
    JWT_SECRET_KEY: str = Field(..., description="Secret key for signing JWTs")
    
    # The algorithm used for JWT signing.
    JWT_ALGORITHM: str = Field("HS256", description="Algorithm for signing JWTs")
    
    # Defines the lifespan of an access token in minutes. Default is 7 days.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24 * 7,
        description="Access token lifespan in minutes (default: 7 days)"
    )

    # --- CORS (Cross-Origin Resource Sharing) Configuration ---
    # A list of origins that are allowed to make requests to the backend.
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="List of allowed CORS origins"
    )

    # --- AI Services Configuration (Optional) ---
    # The API key for connecting to OpenAI's services.
    # This is optional and only required if AI features are enabled.
    OPENAI_API_KEY: Optional[str] = Field(None, description="API key for OpenAI services")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False # Environment variables are case-insensitive
    )

# Create a single, importable instance of the settings
settings = Settings()