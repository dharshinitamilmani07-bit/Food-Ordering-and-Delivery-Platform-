from database import get_db


def register_user(name, email, password):
    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))

        conn.commit()
        return True

    except Exception:
        return False

    finally:
        conn.close()


def login_user(email, password):
    conn = get_db()

    user = conn.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
    """, (email, password)).fetchone()

    conn.close()

    return user