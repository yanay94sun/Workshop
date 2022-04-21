class DomainPaymentInfo:
    def __init__(self, payment_info):
        self.customer_id = payment_info.customer_id
        self.customer_name = payment_info.customer_name
        self.credit_card = payment_info.credit_card
        self.expiration_date = payment_info.expiration_date
        self.cvv = payment_info.cvv
        self.amount_to_pay = payment_info.amount_to_pay
