from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.Visitor import Visitor


class UserController:
    def __init__(self):
        """

        """
        self.users = {}
        self.id_counter = 0

    def create_gust(self):
        id = self.generate_id()
        user = Visitor(id)
        self.users[id] = user
        return Response(value=id)

    def generate_id(self):
        self.id_counter += 1
        return str(self.id_counter)
