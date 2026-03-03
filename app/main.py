from fastapi import FastAPI
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.api.routes import router

setup_logging()

app = FastAPI(
    title="Address Book API",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}