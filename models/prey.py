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

    def get_next_locations(self, state):
        """
        returns the next possible locations for the prey, given a certain state
        :param location:
        :return: all probabilities and according next states
        """
        cur_pred_loc, cur_prey_loc = state
        next_prey_locations  = [ self.field.get_new_coordinates(cur_prey_loc, a) for a in self.get_actions()]
        #the prey can't move to the predator
        if cur_pred_loc in next_prey_locations:
            next_prey_locations.remove(cur_pred_loc)
        return next_prey_locations