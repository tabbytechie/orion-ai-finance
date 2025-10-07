from pydantic import PostgresDsn, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str = Field(..., env="VITE_SUPABASE_URL")
    SUPABASE_KEY: str = Field(..., env="VITE_SUPABASE_PUBLISHABLE_KEY")
    SUPABASE_DB_URL: str = Field(..., env="DATABASE_URL")
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # OpenAI Configuration (optional)
    OPENAI_API_KEY: Optional[str] = None
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database Configuration
    DATABASE_URL: str = ""
    
    @field_validator("DATABASE_URL")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values) -> str:
        if isinstance(v, str) and v:
            return v
        
        # Fallback to Supabase DB URL if DATABASE_URL is not set
        return values.data.get("SUPABASE_DB_URL", "")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()