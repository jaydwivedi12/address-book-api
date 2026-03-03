import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
from app.api.routes import router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Address Book API",
    version="1.0.0",
)

app.include_router(router)


# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(
        "Incoming request: method=%s path=%s",
        request.method,
        request.url.path,
    )

    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled exception during request processing")
        raise

    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        "Completed request: method=%s path=%s status=%s duration_ms=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response


# Global SQLAlchemy Exception Handler
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("Database error occurred")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal database error"},
    )


# Catch-All Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected server error")
    return JSONResponse(
        status_code=500,
        content={"detail": "Unexpected internal server error"},
    )


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}