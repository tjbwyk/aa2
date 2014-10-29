__author__ = 'fbuettner'
from player import Player
from policy import Policy


class Prey(Player):
    """
    The prey class
    """
    def __init__(self, x, y):
        super(Prey, self).__init__(x, y)

    # TODO update policy when predator is next to prey

