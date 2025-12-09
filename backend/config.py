"""
Configuration management for the GitHub Issue Assistant.
Handles environment variables and application settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")  # Optional, for higher rate limits
    
    # Application Settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # LLM Settings
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    
    # Cache Settings
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
        return True


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"⚠️  Configuration Warning: {e}")
