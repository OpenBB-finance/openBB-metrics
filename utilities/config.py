import os
import sys
from pydantic import BaseSettings


def create_path(*path: str) -> str:
    base_path = os.path.dirname(os.path.abspath(__file__))
    above_path = os.path.dirname(base_path)
    default_path = os.path.join(above_path, *path)
    return default_path


class Settings(BaseSettings):
    MONTHLY_FREE_COMMAND: int = 10
    DAILY_FREE_COMMAND: int = 2

    # Loaded from env
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_URL: str
    POSTGRES_DB: str
    TWITTER_BEARER_TOKEN: str
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_USER_AGENT:  str


file = ".env"
if "pytest" in sys.modules:
    file = "test" + file
settings = Settings(_env_file=create_path(file))
