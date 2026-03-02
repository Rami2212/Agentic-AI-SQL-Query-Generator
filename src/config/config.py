import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _req(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

@dataclass(frozen=True)
class Settings:
    APP_URL: str

    MYSQL_HOST: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_PORT: str

    AICC_API_KEY: str
    AICC_BASE_URL: str
    AI_MODEL: str

def get_settings() -> Settings:
    return Settings(
        APP_URL=_req("APP_URL"),
        MYSQL_HOST=_req("MYSQL_HOST"),
        MYSQL_DATABASE=_req("MYSQL_DB"),
        MYSQL_USER=_req("MYSQL_USER"),
        MYSQL_PASSWORD=_req("MYSQL_PASSWORD"),
        MYSQL_PORT=os.getenv("MYSQL_PORT", "3306"),
        AICC_API_KEY=_req("AICC_API_KEY"),
        AICC_BASE_URL=_req("AICC_BASE_URL"),
        AI_MODEL=_req("AI_MODEL")
    )
