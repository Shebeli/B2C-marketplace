class CommandNotAllowedException(Exception):
    def __init__(self, message='Command is not allowed.'):
        self.message = message
        super().__init__(self.message)

    