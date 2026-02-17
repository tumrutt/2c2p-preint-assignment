# fixed currency exchange rate for simplicity
RATE_TO_THB = {
        "THB": 1,
        "USD": 30,
        "EUR": 40,
    }


def calculate_statistics(transactions, currency):
    # change amount to match appropriate currency, then calculate min, max, average
    min_value = None
    max_value = None
    sum_value = 0
    for amount, source_currency in transactions:
        # convert to the wanted currency
        if source_currency != currency:
            amount = amount * RATE_TO_THB[source_currency] / RATE_TO_THB[currency]

        # update min, max
        if max_value is None or amount > max_value:
            max_value = amount
        if min_value is None or amount < min_value:
            min_value = amount

        sum_value += amount

    return {
        "count": len(transactions),
        "currency": currency,
        "min": min_value,
        "max": max_value,
        "average": sum_value / len(transactions),
    }
