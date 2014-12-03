__author__ = 'fbuettner'
from models.player import Player


class Prey(Player):
    """
    The prey class
    """

    def __init__(self, location):
        super(Prey, self).__init__(location, tripping_prob=0.2)

    def __str__(self):
        return "Prey"