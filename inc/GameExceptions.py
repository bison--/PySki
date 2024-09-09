
class InvalidSpriteTypeException(Exception):
    def __init__(self, message="Invalid sprite type"):
        self.message = message
        super().__init__(self.message)
