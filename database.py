import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "urls.db")


def get_db_connection():
    """SQLite database se connection banata hai."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """urls table banata hai agar pehle se nahi bani hui."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            clicks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def save_url(original_url: str, short_code: str):
    """Naya original URL aur short code database mein save karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code),
    )
    conn.commit()
    conn.close()


def get_url_by_code(short_code: str):
    """Short code se original record dhoondhta hai. Agar nahi mila toh None return karta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()
    return row


def increment_clicks(short_code: str):
    """Jab koi link open kare, toh clicks count 1 se badha deta hai."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
        (short_code,),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database and table ready!")