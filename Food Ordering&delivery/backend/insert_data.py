from database import connect, create_tables

create_tables()

con = connect()
cur = con.cursor()


# RESTAURANTS

cur.execute("""
INSERT INTO restaurants(name, location, phone)
VALUES (?, ?, ?)
""", (
    "Anjappar",
    "Chennai",
    "9876543210"
))


cur.execute("""
INSERT INTO restaurants(name, location, phone)
VALUES (?, ?, ?)
""", (
    "A2B",
    "Trichy",
    "9876543211"
))


# ANJAPPAR FOODS

cur.execute("""
INSERT INTO foods(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (
    1,
    "Chicken Biryani",
    180,
    "Biryani"
))


cur.execute("""
INSERT INTO foods(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (
    1,
    "Chicken 65",
    150,
    "Starter"
))


cur.execute("""
INSERT INTO foods(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (
    1,
    "Mutton Biryani",
    250,
    "Biryani"
))


# A2B FOODS

cur.execute("""
INSERT INTO foods(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (
    2,
    "Masala Dosa",
    80,
    "Tiffin"
))


cur.execute("""
INSERT INTO foods(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (
    2,
    "Veg Meals",
    120,
    "Meals"
))


cur.execute("""
INSERT INTO foods(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (
    2,
    "Paneer Fried Rice",
    160,
    "Rice"
))


con.commit()
con.close()

print("Data inserted successfully!")