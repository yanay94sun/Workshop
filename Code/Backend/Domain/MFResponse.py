class Response:
    @staticmethod
    def from_error(error_msg):
        return Response(msg=error_msg)

    def __init__(self, value=None, msg=None):
        """

        """
        self.value = value
        self.msg = msg

    def error_occurred(self):
        return self.msg is not None

