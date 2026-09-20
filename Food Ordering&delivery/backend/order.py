from database import get_db


def create_order(user_id, cart, payment_method, address):

    conn = get_db()

    total = 0
    items = []

    for food_id, quantity in cart.items():

        food = conn.execute("""
            SELECT * FROM foods
            WHERE id=?
        """, (food_id,)).fetchone()

        if food:
            price = food["price"]
            total += price * quantity

            items.append((
                food["id"],
                quantity,
                price
            ))

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders
        (user_id, total, payment_method, status, address)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        total,
        payment_method,
        "Order Placed",
        address
    ))

    order_id = cur.lastrowid

    for food_id, quantity, price in items:

        cur.execute("""
            INSERT INTO order_items
            (order_id, food_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            food_id,
            quantity,
            price
        ))

    conn.commit()
    conn.close()

    return order_id


def get_user_orders(user_id):

    conn = get_db()

    orders = conn.execute("""
        SELECT *
        FROM orders
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    conn.close()

    return orders


def get_order(order_id):

    conn = get_db()

    order = conn.execute("""
        SELECT * FROM orders
        WHERE id=?
    """, (order_id,)).fetchone()

    conn.close()

    return order