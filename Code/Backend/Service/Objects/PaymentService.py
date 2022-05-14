from Code.Backend.Service.Objects.Card import Card


class PaymentService:
    def __init__(self):

        self.__valid_cards = {"4580123456789123": Card("4580123456789123", 10000, "123"),
                              "4580223456789123": Card("4580223456789123", 10000, "123"),
                              "4580323456789123": Card("4580323456789123", 10000, "123"),
                              "4580423456789123": Card("4580423456789123", 10000, "123"),
                              "4580523456789123": Card("4580523456789123", 10000, "123")
                              }

    def is_valid_card(self, card_num, cvv):
        # card = self.__valid_cards[card_num]
        if card_num in self.__valid_cards and cvv == self.__valid_cards[card_num].get_cvv():
            return True
        return False

    def check_founds(self, card_num, amount):
        if self.__valid_cards[card_num].get_balance() < amount:
            return False
        return True

    def pay(self, card_num, cvv, amount):
        if self.is_valid_card(card_num, cvv) and self.check_founds(card_num, amount):
            self.__valid_cards[card_num].pay(amount)
            return True
        return False

    def make_connection(self):
        # mock, just for example
        if 1 > 0:
            return self
        else:
            return None
