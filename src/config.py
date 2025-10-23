import os
from dotenv import load_dotenv
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    
    # CORS Settings
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    # Security Settings
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = os.getenv("SECRET_KEY", JWT_SECRET_KEY)
    
    def __init__(self):
        """Validate required settings"""
        if not self.DATABASE_URL:
            print("ERROR: DATABASE_URL is not set in .env file", file=sys.stderr)
            print("Please check your .env file and ensure DATABASE_URL is configured", file=sys.stderr)
        
        if not self.JWT_SECRET_KEY:
            print("WARNING: JWT_SECRET_KEY is not set in .env file", file=sys.stderr)
            print("Using default key - NOT SECURE FOR PRODUCTION!", file=sys.stderr)


settings = Settings()
