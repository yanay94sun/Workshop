class Product:
    def __init__(self, ID):
        """
        """
        self.__ID = ID
        self.__name = "default name"
        self.__description = ""
        self.__rating = None

    def change_name(self,new_name):
        self.__name = new_name

    def change_description(self,new_description):
        self.__description = new_description

    def change_rating(self,new_rating):
        self.__rating = new_rating
