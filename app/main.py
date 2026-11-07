from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes import auth, users, categories, transactions, summary


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Personal Expense Tracker",
    description="A multi-user API for managing personal income and expenses.",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(summary.router)


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