class Card:
    def __init__(self, card_num, balance, cvv):
        self.__card_num = card_num
        self.__balance = balance
        self.__cvv = cvv

    def pay(self, amount):
        print(amount)
        print(self.__balance)
        self.__balance -= amount

    def get_number(self):
        return self.__card_num

    def get_cvv(self):
        return self.__cvv

    def get_balance(self):
        return self.__balance
