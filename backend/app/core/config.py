from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys (required for full functionality)
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 20
    MAX_TOKENS_PER_REQUEST: int = 6000
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # App Settings
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    MAX_CONCURRENT_AGENTS: int = 5
    
    # Model Settings
    DEFAULT_OPENAI_MODEL: str = "gpt-4o-mini"
    DEFAULT_GEMINI_MODEL: str = "gemini-2.5-flash"
    DEFAULT_GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # External APIs (optional)
    GROQ_API_KEY: str = "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"
    CLINICAL_TRIALS_API_KEY: str = ""
    PUBMED_API_KEY: str = ""
    NCBI_API_KEY: str = "" # Alias for PUBMED
    USPTO_API_KEY: str = ""
    LENS_API_KEY: str = "LUzuObPkoRaZg31cRg4uBf1eZ4o5uPrR3RLotRoPj2XUtYQvGhYC"
    COMTRADE_API_KEY: str = "d4bc07106fdc4759b2e1198f5a6d1434"
    UN_COMTRADE_SUBSCRIPTION_KEY: str = "d4bc07106fdc4759b2e1198f5a6d1434" # Alias for COMTRADE
    
    # Data Mode
    DATA_MODE: str = "mock"  # "mock" or "real"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()