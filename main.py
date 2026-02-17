from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from database import get_db_connection, init_db
from services import calculate_statistics, RATE_TO_THB


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


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
        transactions = cur.fetchall()

    if not transactions:
        raise HTTPException(
            status_code=404,
            detail=f"No transactions found"
        )


    return calculate_statistics(transactions, currency)
