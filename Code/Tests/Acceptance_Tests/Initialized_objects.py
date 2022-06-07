import datetime

from Code.Backend.Service.Objects.PackageInfo import PackageInfo
from Code.Backend.Service.Objects.PaymentInfo import PaymentInfo

admin_user = "admin"
admin_pass = "123"
customer_id_nitzan = "205952971"
nitzan = "Nitzan"
lary = "Lary"
default_product_name = "default name"
credit_card = "1234123412341234"
store_name = "my_store"
product1_id = {"product1_id"}
product1_name = "product1"
product2_id = "product2_id"
today = datetime.date.today()

add_new_product_args = {
    "product_name": default_product_name,
    "product_description": "some product description",
    "price": 10,
    "category": "bread"
}

# tomorrow
try:
    tomorrow = today.replace(day=today.day + 1)
except ValueError:  # e.g 31.1 + 1 !- 32.1
    day = 1
    month = today.month + 1 if today.month != 12 else 1
    year = today.year + 1 if month == 1 else today.year
    tomorrow = today.replace(year=year, month=month, day=day)

next_year = today.replace(year=today.year + 1)
last_year = today.replace(year=today.year - 1)


def good_payment(amount):
    return PaymentInfo(
        **{
            "customer_id": customer_id_nitzan,
            "customer_name": nitzan,
            "credit_card": credit_card,
            "cvv": 123,
            "amount_to_pay": amount
        }
    )


good_payment_info = PaymentInfo(
    **{
        "customer_id": customer_id_nitzan,
        "customer_name": nitzan,
        "credit_card": credit_card,
        "cvv": 123,
        "amount_to_pay": 100
    }
)

bad_amount_payment_info = PaymentInfo(
    **{
        "customer_id": customer_id_nitzan,
        "customer_name": nitzan,
        "credit_card": credit_card,
        "cvv": 123,
        "amount_to_pay": -100
    }
)

# good_package_info = PackageInfo(
#
# )
#
# bad_package_info = PackageInfo(
#
# )

good_register_info = dict(
    {
        "username": nitzan,
        "password": "nitzanPass"
    }
)

good_register_info2 = dict(
    {
        "username": "Asaf",
        "password": "AsafPass"
    }
)
