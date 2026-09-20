from database import get_db


def add_review(user_id, restaurant_id, rating, comment):

    con = get_db()

    con.execute("""
        INSERT INTO reviews
        (user_id,restaurant_id,rating,comment)
        VALUES(?,?,?,?)
    """, (
        user_id,
        restaurant_id,
        rating,
        comment
    ))

    con.commit()
    con.close()


def get_reviews(restaurant_id):

    con = get_db()

    rows = con.execute("""
        SELECT reviews.*,
               users.name AS user_name
        FROM reviews
        JOIN users
        ON users.id=reviews.user_id
        WHERE restaurant_id=?
        ORDER BY reviews.id DESC
    """, (restaurant_id,)).fetchall()

    con.close()
    return rows