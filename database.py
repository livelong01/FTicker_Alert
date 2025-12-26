import sqlite3
from datetime import datetime
from email_alert import send_price_alert

DB_NAME = "flights.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=15)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route TEXT,
            departure_date TEXT,
            return_date TEXT,
            price_current REAL,
            price_min REAL,
            airline TEXT,
            stops INTEGER,
            profile TEXT,
            last_seen TEXT,
            UNIQUE(route, departure_date, return_date, airline, profile)
        )
    """)


def upsert_flight(conn, data):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT price_min FROM flights_history
        WHERE route = ?
          AND departure_date = ?
          AND return_date = ?
          AND airline = ?
          AND profile = ?
    """, (
        data["route"],
        data["departure_date"],
        data["return_date"],
        data["airline"],
        data["profile"]
    ))

    row = cursor.fetchone()
    now = datetime.now().isoformat(timespec="seconds")

    if row:
        old_min = row[0]
        new_min = min(old_min, data["price_current"])

        # 🔔 DISPARA ALERTA SE BAIXOU
        if data["price_current"] < old_min:
            send_price_alert(
                {
                    **data,
                    "last_seen": now
                },
                old_price=old_min
            )

        cursor.execute("""
            UPDATE flights_history
            SET price_current = ?, price_min = ?, last_seen = ?
            WHERE route = ?
            AND departure_date = ?
            AND return_date = ?
            AND airline = ?
            AND profile = ?
        """, (
            data["price_current"],
            new_min,
            now,
            data["route"],
            data["departure_date"],
            data["return_date"],
            data["airline"],
            data["profile"]
        ))