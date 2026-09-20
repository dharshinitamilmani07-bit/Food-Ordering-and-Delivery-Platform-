import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "food_delivery.db"
)

# =========================================================
# EXACT FOOD NAME -> EXACT FOOD IMAGE
# =========================================================

FOOD_IMAGES = {

    "Chicken Biryani":
        "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=900&q=90",

    "Butter Chicken":
        "https://images.unsplash.com/photo-1603894584373-5ac82b1ae398?auto=format&fit=crop&w=900&q=90",

    "Chicken 65":
        "https://images.unsplash.com/photo-1608039755401-742074f0548d?auto=format&fit=crop&w=900&q=90",

    # Dosa - Dosa image
    "Masala Dosa":
        "https://images.unsplash.com/photo-1630383249896-424e482df921?auto=format&fit=crop&w=900&q=90",

    # Idli - Idli image
    "Idli":
        "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=900&q=90",

    # Pongal - separate Pongal search image
    "Pongal":
        "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?auto=format&fit=crop&w=900&q=90",

    "Mutton Biryani":
        "https://images.unsplash.com/photo-1563379091339-03246963d96c?auto=format&fit=crop&w=900&q=90",

    "Paneer Butter Masala":
        "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=900&q=90",

    "Cheese Pizza":
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=90",

    "Veg Pizza":
        "https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=900&q=90",

    "Veg Burger":
        "https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=900&q=90",

    "French Fries":
        "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=900&q=90",

    "Fried Rice":
        "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=900&q=90",

    "Chicken Fried Rice":
        "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=900&q=90",

    "Veg Fried Rice":
        "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=900&q=90",

    "Chicken Noodles":
        "https://images.unsplash.com/photo-1552611052-33e04de081de?auto=format&fit=crop&w=900&q=90",

    "Chicken Tikka":
        "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=900&q=90",

    "Tandoori Chicken":
        "https://images.unsplash.com/photo-1598514982901-ae627c7a4c25?auto=format&fit=crop&w=900&q=90",

    "Veg Meals":
        "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=900&q=90",

    # Samosa - Samosa image
    "Samosa":
        "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=90"
}


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add image column if it does not already exist
try:
    cursor.execute("ALTER TABLE foods ADD COLUMN image TEXT")
except sqlite3.OperationalError:
    pass


# =========================================================
# UPDATE ONLY BY EXACT FOOD NAME
# =========================================================

print("\n======================================")
print("UPDATING FOOD IMAGES")
print("======================================\n")

for food_name, image_url in FOOD_IMAGES.items():

    cursor.execute(
        """
        UPDATE foods
        SET image = ?
        WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
        """,
        (image_url, food_name)
    )

    if cursor.rowcount > 0:
        print("✓", food_name, "-> CORRECT IMAGE")
    else:
        print("✗", food_name, "-> NOT FOUND")


conn.commit()


# =========================================================
# SHOW CURRENT DATABASE MAPPING
# =========================================================

print("\n======================================")
print("CURRENT FOOD IMAGE MAPPING")
print("======================================\n")

cursor.execute("""
    SELECT id, name, image
    FROM foods
    ORDER BY id
""")

rows = cursor.fetchall()

for food_id, name, image in rows:
    print(f"{food_id}. {name}")
    print(f"   IMAGE = {image}")
    print()


conn.close()

print("======================================")
print("DONE - FOOD IMAGES UPDATED")
print("======================================")