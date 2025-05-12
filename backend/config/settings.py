from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "AI Chief of Staff API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # Frontend URL
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    
    # Supabase settings
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    # Pinecone settings
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    
    # OpenAI settings for AutoGen
    OPENAI_API_KEY: str
    
    # Database URL
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 