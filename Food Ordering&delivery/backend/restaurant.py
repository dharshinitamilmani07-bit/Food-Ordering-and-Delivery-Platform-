from database import get_db


def get_restaurants():
    conn = get_db()

    restaurants = conn.execute("""
        SELECT * FROM restaurants
        ORDER BY rating DESC
    """).fetchall()

    conn.close()

    return restaurants


def get_restaurant(restaurant_id):
    conn = get_db()

    restaurant = conn.execute("""
        SELECT * FROM restaurants
        WHERE id=?
    """, (restaurant_id,)).fetchone()

    conn.close()

    return restaurant