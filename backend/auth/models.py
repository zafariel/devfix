from werkzeug.security import generate_password_hash, check_password_hash

from backend.database import get_connection


def init_auth_tables():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                plan TEXT NOT NULL DEFAULT 'free',
                subscription_status TEXT NOT NULL DEFAULT 'inactive',
                message_limit INTEGER NOT NULL DEFAULT 0,
                messages_used INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def create_password_hash(password):
    return generate_password_hash(password)


def verify_password(password, password_hash):
    return check_password_hash(password_hash, password)


def create_user(email, password):
    password_hash = create_password_hash(password)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (
                email,
                password_hash
            )
            VALUES (?, ?)
            """,
            (email, password_hash)
        )

        connection.commit()

        return cursor.lastrowid
    finally:
        connection.close()


def get_user_by_email(email):
    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()
    finally:
        connection.close()
