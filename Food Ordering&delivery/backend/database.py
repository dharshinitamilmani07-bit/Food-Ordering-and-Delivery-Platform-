import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "food_delivery.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            phone TEXT,
            rating REAL DEFAULT 4.0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            description TEXT,
            image TEXT,
            FOREIGN KEY (restaurant_id)
            REFERENCES restaurants(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'Order Placed',
            address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (food_id) REFERENCES foods(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (food_id) REFERENCES foods(id)
        )
    """)

    # Admin
    admin = cur.execute(
        "SELECT id FROM users WHERE email=?",
        ("admin@gmail.com",)
    ).fetchone()

    if not admin:
        cur.execute("""
            INSERT INTO users(name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "Admin",
            "admin@gmail.com",
            "admin123",
            "admin"
        ))

    # Restaurants
    count = cur.execute(
        "SELECT COUNT(*) FROM restaurants"
    ).fetchone()[0]

    if count == 0:

        restaurants = [
            ("Anjappar", "Trichy Road", "9876543210", 4.5),
            ("Saravana Bhavan", "Main Road", "9876543211", 4.4),
            ("Royal Biryani", "Central Bus Stand", "9876543212", 4.6),
            ("Pizza Hub", "Cantonment", "9876543213", 4.2),
            ("Burger Point", "Thillai Nagar", "9876543214", 4.3),
            ("Sweet Oven", "KK Nagar", "9876543215", 4.5)
        ]

        cur.executemany("""
            INSERT INTO restaurants
            (name, location, phone, rating)
            VALUES (?, ?, ?, ?)
        """, restaurants)

    # Foods
    food_count = cur.execute(
        "SELECT COUNT(*) FROM foods"
    ).fetchone()[0]

    if food_count == 0:

        foods = [
            (1, "Masala Dosa", 80, "South Indian",
             "Crispy dosa with tasty potato masala",
             "https://images.unsplash.com/photo-1668236543090-82eba5ee5976"),

            (1, "Paneer Dosa", 120, "South Indian",
             "Dosa filled with delicious paneer",
             "https://images.unsplash.com/photo-1601050690597-df0568f70950"),

            (1, "Idli Sambar", 60, "South Indian",
             "Soft idli served with hot sambar",
             "https://images.unsplash.com/photo-1589301760014-d929f3979dbc"),

            (1, "Medu Vada", 70, "South Indian",
             "Crispy traditional vada",
             "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7"),

            (2, "Ven Pongal", 75, "South Indian",
             "Traditional hot pongal",
             "https://images.unsplash.com/photo-1630383249896-424e482df921"),

            (2, "Poori Masala", 80, "Breakfast",
             "Fluffy poori with potato masala",
             "https://images.unsplash.com/photo-1626132647523-66f5bf380027"),

            (3, "Chicken Biryani", 180, "Biryani",
             "Aromatic chicken biryani",
             "https://images.unsplash.com/photo-1563379091339-03246963d51a"),

            (3, "Mutton Biryani", 240, "Biryani",
             "Rich and spicy mutton biryani",
             "https://images.unsplash.com/photo-1589302168068-964664d93dc0"),

            (3, "Egg Biryani", 130, "Biryani",
             "Flavorful egg biryani",
             "https://images.unsplash.com/photo-1599043513900-ed6fe01d3833"),

            (4, "Margherita Pizza", 220, "Pizza",
             "Classic cheese pizza",
             "https://images.unsplash.com/photo-1574071318508-1cdbab80d002"),

            (4, "Farmhouse Pizza", 280, "Pizza",
             "Loaded vegetable farmhouse pizza",
             "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"),

            (5, "Chicken Burger", 160, "Burger",
             "Juicy chicken burger",
             "https://images.unsplash.com/photo-1568901346375-23c9450c58cd"),

            (5, "Cheese Burger", 140, "Burger",
             "Cheesy classic burger",
             "https://images.unsplash.com/photo-1550547660-d9450f859349"),

            (6, "Chocolate Cake", 120, "Dessert",
             "Rich chocolate cake",
             "https://images.unsplash.com/photo-1578985545062-69928b1d9587"),

            (6, "Gulab Jamun", 80, "Dessert",
             "Soft gulab jamun",
             "https://images.unsplash.com/photo-1601303516534-4b5b1f4b6a9f")
        ]

        cur.executemany("""
            INSERT INTO foods
            (restaurant_id, name, price, category, description, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, foods)

    conn.commit()
    conn.close()