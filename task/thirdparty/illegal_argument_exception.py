class IllegalArgumentException(Exception):

    def __init__(self, message):
        self.message = message
        super(IllegalArgumentException, self).__init__(self.message)
