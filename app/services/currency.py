import logging

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)

FRANKFURTER_URL = "https://api.frankfurter.dev/v2/rates"


async def fetch_exchange_rates(
    base: str,
    quotes: str,
) -> list[dict]:
    params = {
        "base": base,
        "quotes": quotes,
    }

    timeout = httpx.Timeout(10.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                FRANKFURTER_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list):
                raise ValueError("Unexpected response format")

            return data

    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code

        logger.warning(
            "Currency provider returned HTTP %s",
            status_code,
        )

        if status_code in (400, 404, 422):
            raise HTTPException(
                status_code=422,
                detail="One or more currencies are not supported.",
            ) from exc

        raise HTTPException(
            status_code=502,
            detail="Currency provider returned an error.",
        ) from exc

    except httpx.RequestError as exc:
        logger.exception("Could not connect to currency provider")

        raise HTTPException(
            status_code=502,
            detail="Currency provider is unavailable.",
        ) from exc

    except ValueError as exc:
        logger.exception("Currency provider returned invalid JSON data")

        raise HTTPException(
            status_code=502,
            detail="Currency provider returned an invalid response.",
        ) from exc