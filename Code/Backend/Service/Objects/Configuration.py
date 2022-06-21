def create_user(username):
    return {
        "username": username,
        "password": username + "pass"
    }


u1 = create_user("u1")
u2 = create_user("u2")
u3 = create_user("u3")
u4 = create_user("u4")
u5 = create_user("u5")
u6 = create_user("u6")


def add_new_product_args(p_name, price):
    return {
        "product_name": p_name,
        "product_description": "some product description",
        "price": price,
        "category": "some_category"
    }
