from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from database import get_db_connection, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

# fixed currency exchange rate for simplicity
RATE_TO_THB = {
        "THB": 1,
        "USD": 30,
        "EUR": 40,
    }

@app.get("/statistics")
def statistics(currency: str):
    currency = currency.upper()

    if len(currency) != 3:
        raise HTTPException(status_code=400, detail="Currency must be 3 characters")

    if currency not in RATE_TO_THB:
        raise HTTPException(status_code=400, detail="Unsupported currency")

    with get_db_connection() as con:
        cur = con.execute(
            "SELECT payment_amount, currency FROM transactions;"
        )
        res = cur.fetchall()

    if not res:
        raise HTTPException(
            status_code=404,
            detail=f"No transactions found"
        )

    # change amount to match appropriate currency, then calculate min, max, average
    min_value = None
    max_value = None
    sum_value = 0
    for amount, source_currency in res:
        # convert to the wanted currency
        if source_currency != currency:
            amount = amount * RATE_TO_THB[source_currency] / RATE_TO_THB[currency]

        # update min, max
        if max_value is None or amount > max_value:
            max_value = amount
        elif min_value is None or amount < min_value:
            min_value = amount

        sum_value += amount

    return {
        "count": len(res),
        "currency": currency,
        "min": min_value,
        "max": max_value,
        "average": sum_value/len(res),
    }
