import os

from fastapi import FastAPI

from app.api.routers.api import router
from app.db.database import engine
from app.db import tables

app = FastAPI()

# Init DB
tables.Base.metadata.create_all(engine, checkfirst=True)


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=os.environ.get("UVICORN_APP", "main:app"),
        host=os.environ.get("UVICORN_HOST", "0.0.0.0"),
        port=int(os.environ.get("UVICORN_PORT", 8000)),
        workers=int(os.environ.get("UVICORN_WORKERS", 1)),
        reload=bool(os.environ.get("UVICORN_RELOAD", True)),
        log_level=os.environ.get("UVICORN_LOG_LEVEL", "info")
    )
