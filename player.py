__author__ = 'fbuettner'


class Player:
    """
    superclass for predator and prey
    implements common properties like position
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y