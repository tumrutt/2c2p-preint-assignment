import sqlite3
from contextlib import contextmanager

DB_NAME = "database.db"


@contextmanager
def get_db_connection():
    con = sqlite3.connect(DB_NAME)
    try:
        yield con
        con.commit()
    finally:
        con.close()



def init_db():
    create_table()
    insert_sample_data()


def create_table():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            payment_amount REAL NOT NULL CHECK (payment_amount > 0),
            currency TEXT NOT NULL CHECK (length(currency) = 3),
            created_at INTEGER NOT NULL
        );
        """

    try:
        with get_db_connection() as con:
            con.execute(create_table_query)
    except sqlite3.Error as e:
        print(f"Database error while creating table: {e}")
        raise


def insert_sample_data():
    id_sample = ["PAYP", "VISA", "MASTERC", "PROMPTP"]
    currency_sample = ["USD", "THB", "EUR"]

    sample_data = (
        (
            f"{id_sample[i%4]}{i:02d}",
            i,
            currency_sample[i%3],
            1767200400+i
        )
        for i in range(1, 51)
    )

    insert_query = """
        INSERT OR IGNORE INTO transactions
        (transaction_id, payment_amount, currency, created_at)
        VALUES (?, ?, ?, ?);
    """

    try:
        with get_db_connection() as con:
            con.executemany(insert_query, sample_data)
    except sqlite3.Error as e:
        print(f"Database error while inserting sample data: {e}")
        raise
