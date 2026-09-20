from database import get_db


def get_delivery_status(order_id):

    conn = get_db()

    order = conn.execute("""
        SELECT id, status, address
        FROM orders
        WHERE id=?
    """, (order_id,)).fetchone()

    conn.close()

    return order