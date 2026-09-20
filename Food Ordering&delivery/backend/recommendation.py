from database import get_db


def get_recommendations():

    conn = get_db()

    foods = conn.execute("""
        SELECT f.*, r.name AS restaurant_name
        FROM foods f
        JOIN restaurants r
        ON f.restaurant_id = r.id
        ORDER BY f.id DESC
        LIMIT 6
    """).fetchall()

    conn.close()

    return foods