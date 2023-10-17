class NotificationError(Exception):
    def __init__(self, title = 'Exception', message = 'An error occured.'):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message
        self.title = title