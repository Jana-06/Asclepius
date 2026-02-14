"""
Application Configuration Settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "SwasthyaFlow AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Use SQLite for local development
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/swasthyaflow.db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    REDIS_URL: str = "redis://localhost:6379/0"

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "ehr-documents"
    MINIO_SECURE: bool = False

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:9000",
        "http://127.0.0.1:9000",
        "http://127.0.0.1:3000",
        "*"  # Allow all for development
    ]

    MODEL_PATH: str = "data/models"
    TRIAGE_MODEL_PATH: str = "data/models/triage_model.pkl"
    SYMPTOM_ENCODER_PATH: str = "data/models/symptom_encoder.pkl"
    SHAP_EXPLAINER_PATH: str = "data/models/shap_explainer.pkl"
    RULE_ENGINE_PATH: str = "data/models/rule_engine.json"

    HIGH_LOAD_THRESHOLD: float = 0.8
    CRITICAL_LOAD_THRESHOLD: float = 0.95
    OUTBREAK_CLUSTER_MIN_SIZE: int = 5
    OUTBREAK_TIME_WINDOW_HOURS: int = 72
    FAIRNESS_AUDIT_INTERVAL_HOURS: int = 24
    DEMOGRAPHIC_PARITY_THRESHOLD: float = 0.1

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

