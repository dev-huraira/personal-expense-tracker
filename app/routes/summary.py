from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Transaction, Category, User
from app.schemas.summary import (
    CategorySpending,
    CurrencySummary,
    MonthlySummaryResponse,
)


router = APIRouter(
    prefix="/summary",
    tags=["Financial Summary"],
)


@router.get("", response_model=MonthlySummaryResponse)
def get_monthly_summary(
    year: int = Query(ge=2000, le=2100),
    month: int = Query(ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    statement = (
        select(Transaction, Category.name)
        .join(Category, Transaction.category_id == Category.id)
        .where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date < end_date,
        )
    )

    rows = db.execute(statement).all()

    totals = {}

    for transaction, category_name in rows:
        currency = transaction.currency

        if currency not in totals:
            totals[currency] = {
                "income": Decimal("0.00"),
                "expenses": Decimal("0.00"),
                "categories": {},
            }

        current = totals[currency]

        if transaction.type == "income":
            current["income"] += transaction.amount

        else:
            current["expenses"] += transaction.amount

            category_key = (
                transaction.category_id,
                category_name,
            )

            current["categories"][category_key] = (
                current["categories"].get(
                    category_key,
                    Decimal("0.00"),
                )
                + transaction.amount
            )

    summaries = []

    for currency, values in totals.items():
        total_income = values["income"]
        total_expenses = values["expenses"]

        category_spending = [
            CategorySpending(
                category_id=category_id,
                category_name=category_name,
                amount=amount,
            )
            for (
                category_id,
                category_name,
            ), amount in values["categories"].items()
        ]

        summaries.append(
            CurrencySummary(
                currency=currency,
                total_income=total_income,
                total_expenses=total_expenses,
                balance=total_income - total_expenses,
                spending_by_category=category_spending,
            )
        )

    return MonthlySummaryResponse(
        year=year,
        month=month,
        summaries=summaries,
    )