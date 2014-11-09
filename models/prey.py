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

    def get_next_locations(self):
        next_locations = [self.field.get_new_coordinates(self.location, action) for action in self.actions]
        for predator in self.field.get_predators():
            if predator.location in next_locations:
                next_locations.remove(predator.location)
        return next_locations
