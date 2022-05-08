from pydantic import BaseModel
from pydantic.class_validators import Optional


class PaymentInfo:
    # def __init__(self, customer_id, customer_name, credit_card, cvv, amount_to_pay):
    #     self.customer_id = customer_id
    #     self.customer_name = customer_name
    #     self.credit_card = credit_card
    #     # self.expiration_date = expiration_date
    #     self.cvv = cvv
    #     self.amount_to_pay = amount_to_pay

    customer_id: str
    customer_name: str
    credit_card: str
    cvv: str
    amount_to_pay: str
