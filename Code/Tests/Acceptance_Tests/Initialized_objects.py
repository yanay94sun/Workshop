import datetime

from Code.Backend.Service.Objects.PackageInfo import PackageInfo
from Code.Backend.Service.Objects.Payment_info import Payment_info

customer_id_nitzan = "205952971"
nitzan = "Nitzan"
lary = "Lary"
credit_card = "1234123412341234"
store_name = "my_store"
product_id = "product_id"
today = datetime.date.today()

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

good_payment_info = Payment_info(
    customer_id_nitzan,
    nitzan,
    credit_card,
    next_year,
    # 123,
    100
)

bad_expiration_payment_info = Payment_info(
    customer_id_nitzan,
    nitzan,
    credit_card,
    last_year,
    # 123,
    100
)

bad_amount_payment_info = Payment_info(
    customer_id_nitzan,
    nitzan,
    credit_card,
    last_year,
    # 123,
    -100
)

good_package_info = PackageInfo(

)

bad_package_info = PackageInfo(

)

good_register_info = dict(
    {
        "username": nitzan,
        "password": "nitzan"
    }
)
