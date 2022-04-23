from Code.Backend.Domain import MFResponse


class Response:
    def __init__(self, response: MFResponse = None, value=None, msg=None):
        """

        """
        if response:
            self.value = response.value
            self.msg = response.msg
        else:
            self.value = value
            self.msg = msg

    def error_occurred(self):
        return self.msg is not None