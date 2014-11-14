from models.player import Player


class Predator(Player):
    """
    The predator class
    """

    def __init__(self, location):
        super(Predator, self).__init__(location)

    def __str__(self):
        return "Predator"

    def get_next_locations(self, state):
        """
        Get all possible next locations after executing an available action.
        :return: a list of location tuples.
        """
        cur_pred_loc, cur_prey_loc = state
        return [ self.field.get_new_coordinates(cur_pred_loc, a) for a in self.get_actions()]