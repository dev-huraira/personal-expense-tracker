from fastapi import FastAPI

app = FastAPI(
    title="Personal Expense Tracker",
    description="A multi-user API for managing personal income and expenses.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Personal Expense Tracker API is running"}