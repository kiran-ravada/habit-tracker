import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("HABITS_DB_PATH", "data/habits.db"))


def _init_db_on_conn(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            task TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        );
        """)


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    _init_db_on_conn(conn)  # ✅ ensures tables exist even for fresh temp DB
    return conn


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    _init_db_on_conn(conn)
    conn.close()