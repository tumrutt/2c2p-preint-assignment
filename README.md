# 2C2P Preinterview Assignment

This project is a simple backend service built with FastAPI that calculates
minimum, maximum, and average payment amounts from a dataset of transactions.

The service supports currency conversion before calculating statistics.

---

## 🚀 Tech Stack

- Python
- FastAPI
- SQLite
- uv (dependency management)
- Docker

---

## ▶️ How to Run the Application

```bash
docker compose up --build
```

---

## 📌 Approach

- Initializes a dataset of 50 deterministic sample transactions
- Stores transactions in SQLite
- Upon request (`GET /statistics?currency=<THB,EUR,USD>`):
  - `SELECT payment_amount, currency` from all transactions from the database
  - loops through each transaction and:
    - converts `payment_amount` to the requested currency
    - compare to min/max and update accordingly
    - add the converted value to `sum_value`
  - By the end of the loop, returns:
    - Minimum payment amount
    - Maximum payment amount
    - Average payment amount (`sum_value/len(all)`)
    - all in the correct currency

- The task also mentioned that the program must be able to "Read the dataset and display", so I made another endpoint `GET /` to return all the data

---

## Assumption

- I assume that the user is an international online shop, so there can be different currencies. With this in mind, I designed the program to be able to obtain statistics in any currency, so that it can be used in any country in case the company expands globally
- I assume a static currency exchange rate to make the program simpler
