class DomainPaymentInfo:
    def __init__(self, payment_info):
        self.id = payment_info.id
        self.holder = payment_info.holder
        self.card_number = payment_info.card_number
        self.ccv = payment_info.ccv
        # self.amount_to_pay = payment_info.amount_to_pay
        self.year = payment_info.year
        self.month = payment_info.month
