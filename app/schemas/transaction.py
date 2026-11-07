from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TransactionType = Literal["income", "expense"]


class TransactionCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)

    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    currency: str = Field(
        default="PKR",
        pattern=r"^[A-Z]{3}$",
    )

    type: TransactionType

    transaction_date: date

    category_id: int = Field(gt=0)


class TransactionUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    amount: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    currency: str | None = Field(
        default=None,
        pattern=r"^[A-Z]{3}$",
    )

    type: TransactionType | None = None

    transaction_date: date | None = None

    category_id: int | None = Field(
        default=None,
        gt=0,
    )


class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    currency: str
    type: TransactionType
    transaction_date: date
    category_id: int

    model_config = ConfigDict(from_attributes=True)