from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db


app = FastAPI(
    title="Personal Expense Tracker",
    description="A multi-user API for managing personal income and expenses.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Personal Expense Tracker API is running"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }