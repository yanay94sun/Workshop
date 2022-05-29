class Product:
    def __init__(self, ID, name, description, price, category, store_ID):
        """
        """
        self.__ID = ID
        self.__name = name
        self.__description = description
        self.__rating = 0
        self.__price = price
        self.__category = category
        self.store_ID = store_ID

    def change_name(self, new_name):
        self.__name = new_name

    def change_description(self, new_description):
        self.__description = new_description

    def change_rating(self, new_rating):
        self.__rating = new_rating

    def change_price(self, new_price):
        self.__price = new_price

    def change_category(self,new_category):
        self.__category = new_category

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_rating(self):
        pass

    def get_price(self):
        return self.__price

    def get_category(self):
        return self.__category

    def get_ID(self):
        return self.__ID
