#!/usr/bin/env python3
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Test with local .env
class TestSettings(BaseSettings):
    MERCADOLIVRE_SITE_ID: str = "default"
    MERCADOLIVRE_CLIENT_ID: str = ""
    
    model_config = SettingsConfigDict(
        env_file=Path(".env"),
        extra="ignore",
    )

if __name__ == "__main__":
    settings = TestSettings()
    print(f"MERCADOLIVRE_SITE_ID: {settings.MERCADOLIVRE_SITE_ID}")
    print(f"MERCADOLIVRE_CLIENT_ID: {settings.MERCADOLIVRE_CLIENT_ID}")
    
    # Check if env file exists
    env_path = Path(".env")
    print(f"\nEnv file exists: {env_path.exists()}")
    
    # Check if MERCADOLIVRE_SITE_ID is in the file
    if env_path.exists():
        with open(env_path) as f:
            content = f.read()
            if "MERCADOLIVRE_SITE_ID" in content:
                print("MERCADOLIVRE_SITE_ID found in .env file")
                # Extract the value
                for line in content.split('\n'):
                    if line.startswith("MERCADOLIVRE_SITE_ID"):
                        print(f"Line: {line}")
