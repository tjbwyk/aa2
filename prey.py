__author__ = 'fbuettner'
from player import Player


class Prey(Player):
    """
    The prey class
    """
    def __init__(self, x, y):
        super(Prey, self).__init__(x, y)

