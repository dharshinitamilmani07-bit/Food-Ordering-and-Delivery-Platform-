def add_to_cart(cart, food_id):
    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    return cart


def update_cart(cart, food_id, quantity):
    food_id = str(food_id)

    if quantity <= 0:
        cart.pop(food_id, None)
    else:
        cart[food_id] = quantity

    return cart


def remove_from_cart(cart, food_id):
    cart.pop(str(food_id), None)
    return cart