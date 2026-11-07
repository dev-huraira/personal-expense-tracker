from decimal import Decimal

from pydantic import BaseModel


class CategorySpending(BaseModel):
    category_id: int
    category_name: str
    amount: Decimal


class CurrencySummary(BaseModel):
    currency: str
    total_income: Decimal
    total_expenses: Decimal
    balance: Decimal
    spending_by_category: list[CategorySpending]


class MonthlySummaryResponse(BaseModel):
    year: int
    month: int
    summaries: list[CurrencySummary]