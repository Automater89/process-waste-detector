"""
config.py -- Load and validate environment variables.
Run directly to verify Azure OpenAI connectivity configuration.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict:
    required_keys = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
    ]
    config = {}
    missing = []
    for key in required_keys:
        value = os.getenv(key)
        if not value:
            missing.append(key)
        config[key] = value
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")
    return config


if __name__ == "__main__":
    try:
        cfg = get_config()
        print("[OK] All environment variables loaded.")
        print(f"  OpenAI endpoint : {cfg['AZURE_OPENAI_ENDPOINT']}")
        print(f"  Deployment      : {cfg['AZURE_OPENAI_DEPLOYMENT']}")
    except EnvironmentError as e:
        print(f"[ERROR] {e}")
