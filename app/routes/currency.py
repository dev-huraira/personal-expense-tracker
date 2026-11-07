import re

from fastapi import APIRouter, HTTPException, Query

from app.schemas.currency import ExchangeRatesResponse
from app.services.currency import fetch_exchange_rates

router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
)


@router.get("/rates", response_model=ExchangeRatesResponse)
async def get_exchange_rates(
    base: str = Query(
        default="PKR",
        min_length=3,
        max_length=3,
    ),
    quotes: str = Query(
        default="USD,EUR",
        min_length=3,
        max_length=100,
    ),
):
    base = base.upper()
    quotes = quotes.upper()

    if not re.fullmatch(r"[A-Z]{3}", base):
        raise HTTPException(
            status_code=422,
            detail="Base currency must be a three-letter code.",
        )

    quote_list = quotes.split(",")

    if not all(re.fullmatch(r"[A-Z]{3}", q) for q in quote_list):
        raise HTTPException(
            status_code=422,
            detail="Each target currency must be a three-letter code.",
        )

    if len(set(quote_list)) != len(quote_list):
        raise HTTPException(
            status_code=422,
            detail="Duplicate target currencies are not allowed.",
        )

    if base in quote_list:
        raise HTTPException(
            status_code=422,
            detail="Base currency cannot also be a target currency.",
        )

    rates = await fetch_exchange_rates(
        base=base,
        quotes=",".join(quote_list),
    )

    return {"rates": rates}