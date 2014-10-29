__author__ = 'fbuettner'
from player import Player
from policy import Policy


class Prey(Player):
    """
    The prey class
    """
    def __init__(self, location):
        super(Prey, self).__init__(location)

    # TODO update policy when predator is next to prey

