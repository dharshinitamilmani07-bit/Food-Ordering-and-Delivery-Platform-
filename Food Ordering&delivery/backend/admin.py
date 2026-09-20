from database import get_db


def get_all_orders():
    conn = get_db()

    orders = conn.execute("""
        SELECT o.*, u.name, u.email
        FROM orders o
        JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC
    """).fetchall()

    conn.close()
    return orders


def update_order_status(order_id, status):
    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET status=?
        WHERE id=?
    """, (status, order_id))

    conn.commit()
    conn.close()