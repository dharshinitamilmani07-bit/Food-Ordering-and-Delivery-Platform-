from database import connect


con = connect()
cur = con.cursor()


# Restaurant 3
cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (3, "Chicken Biryani", 180, "Biryani"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (3, "Chicken Fried Rice", 160, "Rice"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (3, "Chicken 65", 140, "Starter"))


# Restaurant 4
cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (4, "Veg Biryani", 140, "Biryani"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (4, "Paneer Butter Masala", 180, "Gravy"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (4, "Chapathi", 60, "Tiffin"))


# Restaurant 5
cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (5, "Chicken Noodles", 150, "Noodles"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (5, "Egg Fried Rice", 140, "Rice"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (5, "Chicken 65", 150, "Starter"))


# Restaurant 6
cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (6, "Masala Dosa", 80, "Tiffin"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (6, "Idly", 50, "Tiffin"))

cur.execute("""
INSERT INTO foods
(restaurant_id, name, price, category)
VALUES (?, ?, ?, ?)
""", (6, "Veg Meals", 120, "Meals"))


con.commit()
con.close()

print("Food added successfully!")