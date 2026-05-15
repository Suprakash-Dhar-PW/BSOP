import os

class Settings:
    # Environment configs for MCP and third-party tools
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    OMIUM_API_KEY = os.getenv("OMIUM_API_KEY", "")

    # Application settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
settings = Settings()
