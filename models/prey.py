__author__ = 'fbuettner'
from models.player import Player


class Prey(Player):
    """
    The prey class
    """

    def __init__(self, location):
        super(Prey, self).__init__(location)

    def __str__(self):
        return "Prey"

        # TODO update policy when predator is next to prey

