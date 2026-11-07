from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ExchangeRateItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    date: date
    base: str
    quote: str
    rate: float = Field(gt=0)


class ExchangeRatesResponse(BaseModel):
    rates: list[ExchangeRateItem]