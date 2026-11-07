# Personal Expense Tracker API

A multi-user REST API for managing personal income and expenses. Each user can manage their own categories and transactions, view monthly financial summaries, and retrieve currency exchange rates.

## Features

- User registration and login using password hashing and JWT authentication.
- User-specific categories for income and expenses.
- Create, read, update, and delete financial transactions.
- Monthly summaries showing income, expenses, balance, and spending by category.
- Currency exchange rates through the Frankfurter API.
- PostgreSQL database persistence.
- Request validation, error handling, application logging, and automated tests.

## Technology Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT authentication
- pytest
- HTTPX
- Git

## Project Structure

```text
personal-expense-tracker/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── core/
├── tests/
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── README.md
```

## Requirements

- Python 3.11 or later
- PostgreSQL
- Git

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd personal-expense-tracker
```

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root using `.env.example` as a template.

Set your PostgreSQL connection URL and a secure JWT secret in `.env`.

Never commit `.env` or share its secret values.

## Run the Application

```powershell
uvicorn app.main:app --reload
```

The local API is available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Log in and receive an access token |
| GET | `/users/me` | Get the authenticated user's profile |
| POST | `/categories` | Create a category |
| GET | `/categories` | List the user's categories |
| GET | `/categories/{category_id}` | Get a category |
| PATCH | `/categories/{category_id}` | Update a category |
| DELETE | `/categories/{category_id}` | Delete a category |
| POST | `/transactions` | Create a transaction |
| GET | `/transactions` | List the user's transactions |
| GET | `/transactions/{transaction_id}` | Get a transaction |
| PATCH | `/transactions/{transaction_id}` | Update a transaction |
| DELETE | `/transactions/{transaction_id}` | Delete a transaction |
| GET | `/summary` | Get a monthly financial summary |
| GET | `/currency/rates` | Retrieve exchange rates |
| GET | `/health` | Check application and database health |

Protected endpoints require a valid JWT access token. In `/docs`, use the **Authorize** control to provide the token.

## Run Automated Tests

Configure a separate test database using `TEST_DATABASE_URL` in your `.env` file.

Then run:

```powershell
pytest -v
```

**Important:** The test database must be separate from your development or production database. The test setup recreates its tables.

## External Service

Currency exchange rates are retrieved from the Frankfurter API:

https://api.frankfurter.dev/

The application handles external-service failures and returns an appropriate API error.

## Security Notes

- Passwords are stored as password hashes, not plain text.
- JWT secrets and database credentials belong in environment variables.
- User-specific resources are restricted to their owners.
- Do not commit `.env`, access tokens, or database passwords.

## License

Add a license if you decide to distribute this project publicly.
