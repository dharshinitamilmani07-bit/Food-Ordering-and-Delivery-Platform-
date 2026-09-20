from database import get_db


def get_foods(restaurant_id=None, search=""):
    conn = get_db()

    if restaurant_id:
        foods = conn.execute("""
            SELECT f.*, r.name AS restaurant_name
            FROM foods f
            JOIN restaurants r
            ON f.restaurant_id = r.id
            WHERE f.restaurant_id=?
        """, (restaurant_id,)).fetchall()

    elif search:
        search_value = f"%{search}%"

        foods = conn.execute("""
            SELECT f.*, r.name AS restaurant_name
            FROM foods f
            JOIN restaurants r
            ON f.restaurant_id = r.id
            WHERE f.name LIKE ?
               OR f.category LIKE ?
               OR r.name LIKE ?
        """, (
            search_value,
            search_value,
            search_value
        )).fetchall()

    else:
        foods = conn.execute("""
            SELECT f.*, r.name AS restaurant_name
            FROM foods f
            JOIN restaurants r
            ON f.restaurant_id = r.id
        """).fetchall()

    conn.close()

    return foods


def get_food(food_id):
    conn = get_db()

    food = conn.execute("""
        SELECT f.*, r.name AS restaurant_name
        FROM foods f
        JOIN restaurants r
        ON f.restaurant_id = r.id
        WHERE f.id=?
    """, (food_id,)).fetchone()

    conn.close()

    return food