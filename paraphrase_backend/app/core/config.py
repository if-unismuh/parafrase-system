"""
Core configuration management
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Paraphrase API"
    app_description: str = "High-performance text paraphrasing API with DDGS enhancement"
    version: str = "1.0.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # Security
    secret_key: str = Field(..., min_length=32)
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    
    # Database
    database_url: str = Field(..., description="Database connection URL")
    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10
    
    # Redis
    redis_url: str = Field(..., description="Redis connection URL")
    redis_password: Optional[str] = None
    cache_ttl: int = 3600  # 1 hour default TTL
    
    # Celery
    broker_url: str = Field(..., description="Celery broker URL")
    result_backend: str = Field(..., description="Celery result backend URL")
    
    # AI Services
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # DDGS Configuration
    ddgs_enabled: bool = True
    ddgs_region: str = "id-id"
    ddgs_language: str = "id"
    ddgs_max_results: int = 5
    ddgs_safe_search: str = "moderate"
    
    # File handling
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_file_types: List[str] = [".txt", ".docx", ".doc", ".pdf"]
    upload_dir: str = "uploads"
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    rate_limit_per_day: int = 10000
    
    # Text processing limits
    max_text_length: int = 10000
    min_text_length: int = 10
    max_batch_size: int = 100
    
    # Monitoring
    enable_prometheus: bool = True
    prometheus_port: int = 8001
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: Optional[str] = None
    
    # CORS
    cors_origins: List[str] = ["*"]
    cors_credentials: bool = True
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters long')
        return v
    
    @validator('database_url')
    def validate_database_url(cls, v):
        if not v.startswith(('postgresql://', 'postgresql+psycopg2://', 'sqlite:///')):
            raise ValueError('Database URL must be a valid PostgreSQL or SQLite URL')
        return v
    
    @validator('redis_url')
    def validate_redis_url(cls, v):
        if not v.startswith('redis://'):
            raise ValueError('Redis URL must be a valid Redis URL')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra environment variables
        
    def get_database_url(self) -> str:
        """Get database URL with proper formatting"""
        return self.database_url
        
    def get_redis_url(self) -> str:
        """Get Redis URL with proper formatting"""
        url = self.redis_url
        if self.redis_password:
            # Insert password into URL if provided
            url = url.replace('redis://', f'redis://:{self.redis_password}@')
        return url

# Global settings instance
settings = Settings()

# Environment-specific settings
class DevelopmentSettings(Settings):
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"
    database_echo: bool = True

class ProductionSettings(Settings):
    debug: bool = False
    reload: bool = False
    log_level: str = "WARNING"
    rate_limit_per_minute: int = 30
    cors_origins: List[str] = []  # Restrict in production

class TestingSettings(Settings):
    database_url: str = "sqlite:///./test.db"
    redis_url: str = "redis://localhost:6379/1"
    secret_key: str = "test-secret-key-for-testing-only-32-chars"
    rate_limit_per_minute: int = 1000  # No limits for testing

def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()