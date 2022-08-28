import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    UVICORN_APP = os.environ.get("UVICORN_APP", "main:app"),
    UVICORN_HOST = os.environ.get("UVICORN_HOST", "0.0.0.0"),
    UVICORN_PORT = int(os.environ.get("UVICORN_PORT", 8000)),
    UVICORN_WORKERS = int(os.environ.get("UVICORN_WORKERS", 1)),
    UVICORN_RELOAD = bool(os.environ.get("UVICORN_RELOAD", True)),
    UVICORN_LOG_LEVEL = os.environ.get("UVICORN_LOG_LEVEL", "info")
