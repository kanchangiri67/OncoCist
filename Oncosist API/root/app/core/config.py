"""
Configuration module for the application.

This module handles:
- Environment variable loading.
- Database connection settings.
- Automatic fallback to SQLite if PostgreSQL is unavailable.
"""

import os
import psycopg2
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored console output
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application configuration settings.

    - Uses PostgreSQL if available.
    - Falls back to SQLite if PostgreSQL is not accessible.
    """
    
    # Load database URLs from environment variables
    DATABASE_URL_POSTGRES: str = os.getenv("DATABASE_URL_POSTGRES")
    DATABASE_URL_SQLITE: str = os.getenv("DATABASE_URL_SQLITE", "sqlite:///./database.sqlite3")

    # Default to SQLite, but attempt to use PostgreSQL if available
    DATABASE_URL = DATABASE_URL_SQLITE

    if DATABASE_URL_POSTGRES:
        try:
            # Attempt to connect to PostgreSQL
            conn = psycopg2.connect(DATABASE_URL_POSTGRES)
            conn.close()
            DATABASE_URL = DATABASE_URL_POSTGRES  # Use PostgreSQL if successful
        except Exception:
            print("\n" + "-" * 80)
            print(f"{Fore.YELLOW}[Database Warning]:{Style.RESET_ALL} PostgreSQL is not accessible! Falling back to SQLite.")

    # Log the database being used
    print(f"{Fore.GREEN}[Database]:{Style.RESET_ALL} {DATABASE_URL}")
    print("-" * 80 + "\n")


# Global settings instance for application-wide use
settings = Settings()
