from fastapi import FastAPI
import logging
import time

from fastapi import Request

from app.core.logging_config import configure_logging
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unexpected_exception_handler,
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import Base, engine
from app import models
from app.routes import auth, users, categories, transactions, summary,currency

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

configure_logging()

app = FastAPI(
    title="Personal Expense Tracker",
    description="A multi-user API for managing personal income and expenses.",
    version="1.0.0",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "%s %s - Status: %s - Duration: %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "%s %s failed after %.3fs",
            request.method,
            request.url.path,
            duration,
        )

        raise

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler,
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(summary.router)
app.include_router(currency.router)


@app.get("/")
def home():
    return {
        "message": "Personal Expense Tracker API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database": "configured",
    }