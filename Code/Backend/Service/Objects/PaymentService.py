from Code.Backend.Service.Objects.Card import Card


class PaymentService:
    def __init__(self):

        self.__valid_cards = {4580123456789123: Card(10000, 4580123456789123, 123),
                              4580223456789123: Card(10000, 4580223456789123, 123),
                              4580323456789123: Card(10000, 4580323456789123, 123),
                              4580423456789123: Card(10000, 4580423456789123, 123),
                              4580523456789123: Card(10000, 4580523456789123, 123)
                              }

    def is_valid_card(self, card_num, cvv):
        card = self.__valid_cards[card_num]
        if card in self.__valid_cards and cvv == card.get_cvv():
            return True
        return False

    def check_founds(self, card, amount):
        if self.__valid_cards[card.get_number()] < amount:
            return False
        return True

    def pay(self, card, cvv, amount):
        if self.is_valid_card(card, cvv) and self.check_founds(card, amount):
            card.pay(amount)
            return True
        return False

    def make_connection(self, market):
        # mock, just for example
        if 1 > 0:
            return self
        else:
            return None
