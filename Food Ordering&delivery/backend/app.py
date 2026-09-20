from flask import Flask, request, redirect, session, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "foodiego_secret_123"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.path.dirname(BASE_DIR), "food_delivery_fixed.db")


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS restaurants(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            phone TEXT,
            rating REAL DEFAULT 4.5,
            image TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS foods(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT,
            image TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL,
            payment TEXT,
            status TEXT DEFAULT 'Order Placed',
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS order_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            food_id INTEGER,
            quantity INTEGER,
            price REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            food_id INTEGER,
            rating INTEGER,
            comment TEXT
        )
    """)

    # ---------------- ADMIN ----------------

    admin = conn.execute(
        "SELECT id FROM users WHERE email=?",
        ("admin@gmail.com",)
    ).fetchone()

    if not admin:
        conn.execute("""
            INSERT INTO users(name,email,password,role)
            VALUES(?,?,?,?)
        """, ("Admin", "admin@gmail.com", "admin123", "admin"))

    # ---------------- USER ----------------

    user = conn.execute(
        "SELECT id FROM users WHERE email=?",
        ("user@gmail.com",)
    ).fetchone()

    if not user:
        conn.execute("""
            INSERT INTO users(name,email,password,role)
            VALUES(?,?,?,?)
        """, ("Demo User", "user@gmail.com", "1234", "customer"))

    # =====================================================
    # RESTAURANTS
    # =====================================================

    restaurants = [
        (
            "Biryani House",
            "Chennai",
            "9876543210",
            4.7,
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=80"
        ),
        (
            "Sweet Treats",
            "Chennai",
            "9876543211",
            4.6,
            "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=900&q=80"
        ),
        (
            "Anjappar",
            "Chennai",
            "9876543212",
            4.5,
            "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80"
        ),
        (
            "A2B",
            "Chennai",
            "9876543213",
            4.4,
            "https://images.unsplash.com/photo-1552566626-52f8b828add9?auto=format&fit=crop&w=900&q=80"
        ),
        (
            "Pizza Corner",
            "Chennai",
            "9876543214",
            4.3,
            "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=80"
        ),
        (
            "Burger Hub",
            "Chennai",
            "9876543215",
            4.2,
            "https://images.unsplash.com/photo-1571091718767-18b5b1457add?auto=format&fit=crop&w=900&q=80"
        )
    ]

    if conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0] == 0:
        conn.executemany("""
            INSERT INTO restaurants
            (name,location,phone,rating,image)
            VALUES(?,?,?,?,?)
        """, restaurants)

    # =====================================================
    # FOODS
    # =====================================================

    foods = [
        (
            1,
            "Chicken Biryani",
            180,
            "Biryani",
            "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=800&q=80"
        ),
        (
            1,
            "Mutton Biryani",
            240,
            "Biryani",
            "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=800&q=80"
        ),
        (
            1,
            "Chicken 65",
            150,
            "Starters",
            "https://images.unsplash.com/photo-1608039755401-742074f0548d?auto=format&fit=crop&w=800&q=80"
        ),
        (
            2,
            "Masala Dosa",
            90,
            "South Indian",
            "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80"
        ),
        (
            2,
            "Idli",
            60,
            "South Indian",
            "https://images.unsplash.com/photo-1589301773859-9f5b0c1e8f8b?auto=format&fit=crop&w=800&q=80"
        ),
        (
            2,
            "Pongal",
            80,
            "South Indian",
            "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80"
        ),
        (
            3,
            "Butter Chicken",
            220,
            "Chicken",
            "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80"
        ),
        (
            3,
            "Chicken Tikka",
            190,
            "Starters",
            "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=800&q=80"
        ),
        (
            3,
            "Tandoori Chicken",
            250,
            "Chicken",
            "https://images.unsplash.com/photo-1598514982901-ae627c7a4c25?auto=format&fit=crop&w=800&q=80"
        ),
        (
            4,
            "Veg Meals",
            130,
            "Meals",
            "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80"
        ),
        (
            4,
            "Paneer Butter Masala",
            180,
            "North Indian",
            "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=800&q=80"
        ),
        (
            5,
            "Cheese Pizza",
            250,
            "Pizza",
            "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=800&q=80"
        ),
        (
            5,
            "Veg Pizza",
            220,
            "Pizza",
            "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80"
        ),
        (
            6,
            "Veg Burger",
            140,
            "Burger",
            "https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=800&q=80"
        ),
        (
            6,
            "French Fries",
            100,
            "Sides",
            "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80"
        )
    ]

    if conn.execute("SELECT COUNT(*) FROM foods").fetchone()[0] == 0:
        conn.executemany("""
            INSERT INTO foods
            (restaurant_id,name,price,category,image)
            VALUES(?,?,?,?,?)
        """, foods)

    conn.commit()
    conn.close()


# =========================================================
# COMMON HTML
# =========================================================

CSS = """

*{
    box-sizing:border-box;
}

body{
    margin:0;
    font-family:Arial, sans-serif;
    background:#f5f7fb;
    color:#172033;
}

nav{
    height:70px;
    background:white;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 7%;
    box-shadow:0 2px 12px rgba(0,0,0,.08);
    position:sticky;
    top:0;
    z-index:100;
}

.logo{
    font-size:25px;
    font-weight:bold;
    color:#1769d2;
}

.navlinks{
    display:flex;
    gap:22px;
}

.navlinks a{
    text-decoration:none;
    color:#222;
    font-weight:bold;
}

.navlinks a:hover{
    color:#1769d2;
}

.container{
    width:90%;
    max-width:1200px;
    margin:40px auto;
}

.hero{
    background:linear-gradient(135deg,#1268d5,#49a3ff);
    color:white;
    padding:75px 30px;
    text-align:center;
}

.hero h1{
    font-size:48px;
    margin:10px;
}

.hero p{
    font-size:20px;
}

.btn{
    display:inline-block;
    background:white;
    color:#1268d5;
    padding:14px 28px;
    border-radius:10px;
    text-decoration:none;
    font-weight:bold;
    margin-top:20px;
}

.grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:25px;
}

.card{
    background:white;
    border-radius:15px;
    overflow:hidden;
    box-shadow:0 5px 20px rgba(0,0,0,.08);
    transition:.2s;
}

.card:hover{
    transform:translateY(-4px);
}

.card img{
    width:100%;
    height:210px;
    object-fit:cover;
    display:block;
}

.cardbody{
    padding:18px;
}

.cardbody h2{
    margin:5px 0 10px;
}

.price{
    color:#1769d2;
    font-size:19px;
    font-weight:bold;
}

.small{
    color:#777;
}

.button{
    display:block;
    width:100%;
    border:0;
    background:#1769d2;
    color:white;
    padding:13px;
    border-radius:8px;
    text-align:center;
    text-decoration:none;
    font-weight:bold;
    margin-top:14px;
    cursor:pointer;
}

.button:hover{
    background:#0e55ad;
}

.formbox{
    max-width:450px;
    margin:60px auto;
    background:white;
    padding:35px;
    border-radius:15px;
    box-shadow:0 5px 25px rgba(0,0,0,.1);
}

input,select,textarea{
    width:100%;
    padding:13px;
    margin:8px 0 15px;
    border:1px solid #ddd;
    border-radius:8px;
}

.center{
    text-align:center;
}

.cartbox,.orderbox{
    background:white;
    padding:22px;
    margin:20px auto;
    border-radius:14px;
    box-shadow:0 3px 15px rgba(0,0,0,.08);
}

.success{
    max-width:600px;
    margin:80px auto;
    background:white;
    padding:50px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 5px 25px rgba(0,0,0,.1);
}

.status{
    display:inline-block;
    padding:8px 15px;
    border-radius:20px;
    background:#e8f2ff;
    color:#1769d2;
    font-weight:bold;
}

.search{
    max-width:600px;
    margin:0 auto 35px;
}

footer{
    margin-top:60px;
    padding:30px;
    text-align:center;
    background:#172033;
    color:white;
}

@media(max-width:800px){
    .grid{
        grid-template-columns:1fr 1fr;
    }

    .navlinks{
        gap:8px;
        font-size:13px;
    }

    .hero h1{
        font-size:34px;
    }
}

@media(max-width:550px){
    .grid{
        grid-template-columns:1fr;
    }

    nav{
        padding:0 3%;
    }
}
"""


def page(content, title="FoodieGo"):
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ title }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>{{ css }}</style>
    </head>

    <body>

    <nav>
        <div class="logo">🍴 FoodieGo</div>

        <div class="navlinks">
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('restaurants') }}">Restaurants</a>
            <a href="{{ url_for('foods') }}">Food</a>
            <a href="{{ url_for('cart') }}">🛒 Cart</a>
            <a href="{{ url_for('orders') }}">Orders</a>

            {% if session.get("user_id") %}
                <a href="{{ url_for('logout') }}">Logout</a>
            {% else %}
                <a href="{{ url_for('login') }}">Login</a>
            {% endif %}
        </div>
    </nav>

    {{ content|safe }}

    <footer>
        FoodieGo © 2026 | Fresh Food • Fast Delivery
    </footer>

    </body>
    </html>
    """, content=content, title=title, css=CSS)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    content = """
    <section class="hero">
        <h1>Delicious Food Delivered 🍕</h1>
        <p>Order your favourite meals from the best restaurants.</p>

        <a class="btn" href="/restaurants">
            Explore Restaurants
        </a>
    </section>

    <div class="container">
        <h1 class="center">Why FoodieGo?</h1>

        <div class="grid">

            <div class="card">
                <div class="cardbody center">
                    <h2>🍽️ Many Restaurants</h2>
                    <p>Choose from multiple restaurants.</p>
                </div>
            </div>

            <div class="card">
                <div class="cardbody center">
                    <h2>🚚 Fast Delivery</h2>
                    <p>Track your order easily.</p>
                </div>
            </div>

            <div class="card">
                <div class="cardbody center">
                    <h2>💳 Easy Payment</h2>
                    <p>Choose your preferred payment method.</p>
                </div>
            </div>

        </div>
    </div>
    """

    return page(content)


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        try:
            conn.execute("""
                INSERT INTO users(name,email,password)
                VALUES(?,?,?)
            """, (name,email,password))

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            conn.close()

            return page("""
            <div class="formbox center">
                <h2>Email already exists</h2>
                <a href="/register">Try Again</a>
            </div>
            ""","Register")

    return page("""
    <div class="formbox">

        <h1 class="center">Create Account</h1>

        <form method="POST">

            <input name="name"
                   placeholder="Full Name"
                   required>

            <input name="email"
                   type="email"
                   placeholder="Email"
                   required>

            <input name="password"
                   type="password"
                   placeholder="Password"
                   required>

            <button class="button">
                Register
            </button>

        </form>

        <p class="center">
            Already have an account?
            <a href="/login">Login</a>
        </p>

    </div>
    ""","Register")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute("""
            SELECT * FROM users
            WHERE email=? AND password=?
        """,(email,password)).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]

            return redirect(url_for("home"))

        return page("""
        <div class="formbox center">
            <h2>❌ Invalid email or password</h2>
            <a href="/login">Try Again</a>
        </div>
        ""","Login")

    return page("""
    <div class="formbox">

        <h1 class="center">Login</h1>

        <form method="POST">

            <input name="email"
                   type="email"
                   placeholder="Email"
                   required>

            <input name="password"
                   type="password"
                   placeholder="Password"
                   required>

            <button class="button">
                Login
            </button>

        </form>

        <p class="center">
            New user?
            <a href="/register">Create Account</a>
        </p>

        <hr>

        <p class="center">
            Demo User:<br>
            user@gmail.com / 1234
        </p>

        <p class="center">
            Admin:<br>
            admin@gmail.com / admin123
        </p>

    </div>
    ""","Login")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================================================
# RESTAURANTS
# =========================================================

@app.route("/restaurants")
def restaurants():

    conn = get_db()

    data = conn.execute("""
        SELECT * FROM restaurants
        ORDER BY id
    """).fetchall()

    conn.close()

    cards = ""

    for r in data:

        cards += f"""
        <div class="card">

            <img src="{r['image']}"
                 alt="{r['name']}">

            <div class="cardbody">

                <h2>{r['name']}</h2>

                <p class="small">
                    📍 {r['location']}
                </p>

                <p>
                    ⭐ {r['rating']}
                </p>

                <a class="button"
                   href="/menu/{r['id']}">
                    View Menu
                </a>

            </div>
        </div>
        """

    content = f"""
    <div class="container">

        <h1 class="center">
            Restaurants
        </h1>

        <div class="grid">
            {cards}
        </div>

    </div>
    """

    return page(content,"Restaurants")


# =========================================================
# RESTAURANT MENU
# =========================================================

@app.route("/menu/<int:restaurant_id>")
def menu(restaurant_id):

    conn = get_db()

    restaurant = conn.execute("""
        SELECT * FROM restaurants
        WHERE id=?
    """,(restaurant_id,)).fetchone()

    foods = conn.execute("""
        SELECT * FROM foods
        WHERE restaurant_id=?
    """,(restaurant_id,)).fetchall()

    conn.close()

    if not restaurant:
        return page("""
        <div class="container center">
            <h2>Restaurant not found</h2>
        </div>
        """)

    cards = ""

    for food in foods:

        cards += f"""
        <div class="card">

            <img src="{food['image']}"
                 alt="{food['name']}">

            <div class="cardbody">

                <h2>{food['name']}</h2>

                <p class="small">
                    {food['category']}
                </p>

                <p class="price">
                    ₹{food['price']}
                </p>

                <a class="button"
                   href="/add_to_cart/{food['id']}">
                    🛒 Add to Cart
                </a>

            </div>

        </div>
        """

    content = f"""
    <div class="container">

        <h1 class="center">
            {restaurant['name']}
        </h1>

        <p class="center">
            ⭐ {restaurant['rating']} |
            📍 {restaurant['location']}
        </p>

        <div class="grid">
            {cards}
        </div>

    </div>
    """

    return page(content,"Menu")


# =========================================================
# ALL FOODS
# =========================================================

@app.route("/foods")
def foods():

    search = request.args.get("search","").strip()

    conn = get_db()

    if search:

        data = conn.execute("""
            SELECT * FROM foods
            WHERE name LIKE ?
               OR category LIKE ?
        """,(f"%{search}%",f"%{search}%")).fetchall()

    else:

        data = conn.execute("""
            SELECT * FROM foods
            ORDER BY id
        """).fetchall()

    conn.close()

    cards = ""

    for food in data:

        cards += f"""
        <div class="card">

            <img src="{food['image']}"
                 alt="{food['name']}">

            <div class="cardbody">

                <h2>{food['name']}</h2>

                <p class="small">
                    {food['category']}
                </p>

                <p class="price">
                    ₹{food['price']}
                </p>

                <a class="button"
                   href="/add_to_cart/{food['id']}">
                    🛒 Add to Cart
                </a>

            </div>

        </div>
        """

    content = f"""
    <div class="container">

        <h1 class="center">
            Food Menu
        </h1>

        <form class="search" method="GET">

            <input name="search"
                   placeholder="Search food..."
                   value="{search}">

            <button class="button">
                Search
            </button>

        </form>

        <div class="grid">
            {cards}
        </div>

    </div>
    """

    return page(content,"Food")


# =========================================================
# ADD TO CART
# =========================================================

@app.route("/add_to_cart/<int:food_id>")
def add_to_cart(food_id):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(food_id)

    session.modified = True

    return redirect(url_for("cart"))


# Old URL also works
@app.route("/add/<int:id>")
def add(id):

    return redirect(url_for("add_to_cart", food_id=id))


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    cart_ids = session.get("cart", [])

    items = []

    conn = get_db()

    for food_id in cart_ids:

        food = conn.execute("""
            SELECT * FROM foods
            WHERE id=?
        """,(food_id,)).fetchone()

        if food:
            items.append(food)

    conn.close()

    total = sum(float(x["price"]) for x in items)

    cards = ""

    for food in items:

        cards += f"""
        <div class="cartbox">

            <div style="display:flex;gap:20px;align-items:center">

                <img src="{food['image']}"
                     style="width:120px;height:90px;
                     object-fit:cover;border-radius:10px">

                <div>

                    <h2>{food['name']}</h2>

                    <p class="price">
                        ₹{food['price']}
                    </p>

                    <a href="/remove_from_cart/{food['id']}">
                        Remove
                    </a>

                </div>

            </div>

        </div>
        """

    if not items:

        content = """
        <div class="success">

            <h1>🛒 Cart is Empty</h1>

            <p>Add some delicious food first.</p>

            <a class="button"
               href="/foods">
                Browse Food
            </a>

        </div>
        """

    else:

        content = f"""
        <div class="container">

            <h1 class="center">
                🛒 My Cart
            </h1>

            {cards}

            <div class="cartbox center">

                <h1>
                    Total: ₹{total:.2f}
                </h1>

                <a class="button"
                   href="/payment">
                    Proceed to Checkout
                </a>

            </div>

        </div>
        """

    return page(content,"Cart")


# =========================================================
# REMOVE CART
# =========================================================

@app.route("/remove_from_cart/<int:food_id>")
def remove_from_cart(food_id):

    cart_ids = session.get("cart", [])

    if food_id in cart_ids:
        cart_ids.remove(food_id)

    session["cart"] = cart_ids
    session.modified = True

    return redirect(url_for("cart"))


# =========================================================
# PAYMENT / CHECKOUT
# =========================================================

@app.route("/payment", methods=["GET","POST"])
def payment():

    cart_ids = session.get("cart", [])

    if not cart_ids:
        return redirect(url_for("cart"))

    if request.method == "POST":

        method = request.form["payment"]
        address = request.form["address"]

        conn = get_db()

        items = []

        for food_id in cart_ids:

            food = conn.execute("""
                SELECT * FROM foods
                WHERE id=?
            """,(food_id,)).fetchone()

            if food:
                items.append(food)

        total = sum(float(x["price"]) for x in items)

        user_id = session.get("user_id")

        if not user_id:
            conn.close()
            return redirect(url_for("login"))

        cursor = conn.execute("""
            INSERT INTO orders
            (user_id,total,payment,status,address)
            VALUES(?,?,?,?,?)
        """,(
            user_id,
            total,
            method,
            "Order Placed",
            address
        ))

        order_id = cursor.lastrowid

        for food in items:

            conn.execute("""
                INSERT INTO order_items
                (order_id,food_id,quantity,price)
                VALUES(?,?,?,?)
            """,(
                order_id,
                food["id"],
                1,
                food["price"]
            ))

        conn.commit()
        conn.close()

        session["cart"] = []

        return redirect(
            url_for("success", order_id=order_id)
        )

    return page("""
    <div class="formbox">

        <h1 class="center">
            Checkout
        </h1>

        <form method="POST">

            <label>Delivery Address</label>

            <textarea name="address"
                      placeholder="Enter delivery address"
                      required></textarea>

            <label>Payment Method</label>

            <select name="payment" required>

                <option value="">
                    Select Payment
                </option>

                <option>
                    Cash on Delivery
                </option>

                <option>
                    UPI
                </option>

                <option>
                    Credit Card
                </option>

                <option>
                    Debit Card
                </option>

            </select>

            <button class="button">
                Place Order
            </button>

        </form>

    </div>
    ""","Payment")


# =========================================================
# ORDER SUCCESS
# =========================================================

@app.route("/success/<int:order_id>")
def success(order_id):

    return page(f"""
    <div class="success">

        <h1>🎉 Order Placed!</h1>

        <h2>
            Order #{order_id}
        </h2>

        <p>
            Your food order has been successfully placed.
        </p>

        <p>
            🚚 Delivery partner will deliver your food soon.
        </p>

        <a class="button"
           href="/orders">
            Track My Order
        </a>

    </div>
    ""","Order Success")


# =========================================================
# ORDERS
# =========================================================

@app.route("/orders")
def orders():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    conn = get_db()

    orders_data = conn.execute("""
        SELECT * FROM orders
        WHERE user_id=?
        ORDER BY id DESC
    """,(user_id,)).fetchall()

    conn.close()

    cards = ""

    for order in orders_data:

        cards += f"""
        <div class="orderbox">

            <h2>
                Order #{order['id']}
            </h2>

            <p>
                Amount:
                <b>₹{order['total']}</b>
            </p>

            <p>
                Payment:
                {order['payment']}
            </p>

            <p class="status">
                {order['status']}
            </p>

            <p>
                📍 {order['address']}
            </p>

            <a class="button"
               href="/delivery/{order['id']}">
                🚚 Track Delivery
            </a>

        </div>
        """

    if not cards:

        cards = """
        <div class="success">
            <h2>No orders yet.</h2>

            <a class="button"
               href="/foods">
                Order Food
            </a>
        </div>
        """

    return page(f"""
    <div class="container">

        <h1 class="center">
            📦 My Orders
        </h1>

        {cards}

    </div>
    ""","Orders")


# =========================================================
# DELIVERY
# =========================================================

@app.route("/delivery/<int:order_id>")
def delivery(order_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    conn = get_db()

    order = conn.execute("""
        SELECT * FROM orders
        WHERE id=? AND user_id=?
    """,(order_id,user_id)).fetchone()

    conn.close()

    if not order:
        return page("""
        <div class="success">
            <h2>Order not found</h2>
        </div>
        """)

    status = order["status"]

    return page(f"""
    <div class="success">

        <h1>🚚 Live Delivery Tracking</h1>

        <h2>Order #{order_id}</h2>

        <h2 class="status">
            {status}
        </h2>

        <br><br>

        <p>🟢 Order Placed</p>
        <p>🍳 Preparing Food</p>
        <p>🛵 Out for Delivery</p>
        <p>🏠 Delivered</p>

    </div>
    ""","Delivery Tracking")


# =========================================================
# ADMIN
# =========================================================

@app.route("/admin")
def admin():

    if session.get("role") != "admin":
        return page("""
        <div class="success">
            <h2>Admin access only</h2>
        </div>
        """)

    conn = get_db()

    orders_data = conn.execute("""
        SELECT orders.*, users.name, users.email
        FROM orders
        JOIN users ON orders.user_id=users.id
        ORDER BY orders.id DESC
    """).fetchall()

    conn.close()

    rows = ""

    for order in orders_data:

        rows += f"""
        <div class="orderbox">

            <h2>
                Order #{order['id']}
            </h2>

            <p>
                Customer:
                {order['name']}
            </p>

            <p>
                Email:
                {order['email']}
            </p>

            <p>
                Amount:
                ₹{order['total']}
            </p>

            <p>
                Current Status:
                <b>{order['status']}</b>
            </p>

            <form method="POST"
                  action="/admin/status/{order['id']}">

                <select name="status">

                    <option>Order Placed</option>
                    <option>Preparing Food</option>
                    <option>Out for Delivery</option>
                    <option>Delivered</option>

                </select>

                <button class="button">
                    Update Status
                </button>

            </form>

        </div>
        """

    return page(f"""
    <div class="container">

        <h1 class="center">
            👨‍💼 Admin Dashboard
        </h1>

        {rows}

    </div>
    ""","Admin")


# =========================================================
# ADMIN STATUS
# =========================================================

@app.route("/admin/status/<int:order_id>", methods=["POST"])
def update_status(order_id):

    if session.get("role") != "admin":
        return redirect(url_for("home"))

    status = request.form["status"]

    conn = get_db()

    conn.execute("""
        UPDATE orders
        SET status=?
        WHERE id=?
    """,(status,order_id))

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


# =========================================================
# REVIEW
# =========================================================

@app.route("/review/<int:food_id>", methods=["GET","POST"])
def review(food_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":

        rating = request.form["rating"]
        comment = request.form["comment"]

        conn = get_db()

        conn.execute("""
            INSERT INTO reviews
            (user_id,food_id,rating,comment)
            VALUES(?,?,?,?)
        """,(
            user_id,
            food_id,
            rating,
            comment
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("foods"))

    return page("""
    <div class="formbox">

        <h1 class="center">
            ⭐ Write Review
        </h1>

        <form method="POST">

            <label>Rating</label>

            <select name="rating">

                <option value="5">⭐⭐⭐⭐⭐</option>
                <option value="4">⭐⭐⭐⭐</option>
                <option value="3">⭐⭐⭐</option>
                <option value="2">⭐⭐</option>
                <option value="1">⭐</option>

            </select>

            <textarea name="comment"
                      placeholder="Write your review..."
                      required></textarea>

            <button class="button">
                Submit Review
            </button>

        </form>

    </div>
    ""","Review")


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    init_db()

    print("=" * 55)
    print("        FOODIEGO FOOD ORDERING PLATFORM")
    print("=" * 55)
    print("Admin : admin@gmail.com")
    print("Password : admin123")
    print("User  : user@gmail.com")
    print("Password : 1234")
    print("=" * 55)
    print("Open: http://127.0.0.1:5000")
    print("=" * 55)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )