class Response:
    def __init__(self, value=None, msg=None):
        """

        """
        self.value = value
        self.msg = msg

    def error_occurred(self):
        return self.msg is not None

