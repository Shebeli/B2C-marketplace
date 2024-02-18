class MethodNotAllowedException(Exception):
    def __init__(self, message='Method is not allowed.'):
        self.message = message
        super().__init__(self.message)

    