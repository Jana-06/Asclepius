"""Local runner for SwasthyaFlow AI backend (dev)

This script sets minimal env fallbacks and runs uvicorn.
"""

import os
import pathlib

# Ensure working dir is backend
ROOT = pathlib.Path(__file__).parent.resolve()
os.chdir(ROOT)

# Minimal environment defaults for local dev
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./dev_db.sqlite")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("MINIO_ENDPOINT", "http://localhost:9000")
os.environ.setdefault("MODEL_PATH", str(ROOT / "data" / "models"))
os.environ.setdefault("PORT", "8000")

# Start uvicorn
if __name__ == '__main__':
    import uvicorn

    print("Starting SwasthyaFlow AI (local dev) on 127.0.0.1:8080")
    uvicorn.run("app.main:app", host="127.0.0.1", port=int(os.environ.get("PORT", 8080)), reload=True)
