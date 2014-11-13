from models.player import Player


class Predator(Player):
    """
    The predator class
    """

    def __init__(self, location):
        super(Predator, self).__init__(location)

    def __str__(self):
        return "Predator"

    def get_actions(self):
        return [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]

    def get_next_locations(self, state):
        """
        Get all possible next locations after executing an available action.
        :return: a list of location tuples.
        """
        cur_pred_loc, cur_prey_loc = state
        return [ self.field.get_new_coordinates(cur_pred_loc, a) for a in self.get_actions()]

    def act(self):
        """

        :return:
        """
        act, preyact = self.policy.pick_next_action()
        self.location = self.field.get_new_coordinates(self.location, act)
        self.field.update_prey_location(preyact)