import numpy as np

from models.predator import Predator
from models.prey import Prey


def init_default_environment(pred_loc=(0, 0), prey_loc=(5, 5), value_init=30):
    field = Field(11, 11)
    raise NotImplementedError
    return field


class Field(object):
    """
    the playground
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []
        self.steps = 0

    def __str__(self):
        result = map(lambda p: str(p) + "(" + str(p.location[0]) + "," + str(p.location[1]) + ")", self.players)
        return ", ".join(result)

    def act(self, **kwargs):
        raise NotImplementedError

    def get_new_coordinates(self, current_location, delta):
        (x, y) = current_location
        (delta_x, delta_y) = delta
        new_location = (
            (x + delta_x) % self.width,
            (y + delta_y) % self.height
        )
        return new_location


    def get_relative_position(self, location1, location2):
        x1, y1 = location1
        move = ((int(np.floor(self.width / 2)) - x1), (int(np.floor(self.height / 2)) - y1))
        x1, y1 = self.get_new_coordinates(location1, move)
        x2, y2 = self.get_new_coordinates(location2, move)
        return (x2 - x1), (y2 - y1)

    def add_player(self, player):
        player.field = self
        self.players.append(player)

    def get_players(self, exception_player=None):
        return [player for player in self.players if player is not exception_player]

    def get_players_of_class(self, player_class, exception_player=None):
        return [player for player in self.players if
                isinstance(player, player_class) and player is not exception_player]

    def get_predators(self, exception_player=None):
        return self.get_players_of_class(Predator, exception_player)

    def get_preys(self, exception_player=None):
        return self.get_players_of_class(Prey, exception_player)

    def is_ended(self):
        """
        checks if all preys have been found by a predator
        :return: true if game is over
        """
        # 1) Predators collide
        # 2) Predator catches pray
        raise NotImplementedError, "Not sure if this is the right way to go"

    def get_reward(self, state=None):
        """
        returns a reward for the current state given
        :param state:
        :return:
        """
        raise NotImplementedError


    def get_all_states(self):
        raise NotImplementedError

    def get_all_states_without_terminal(self):
        raise NotImplementedError

    def get_current_state(self):
        raise NotImplementedError

    def get_next_states(self, state, pred_action=None):
        """
        returns all next states from the given state that are not illegal
        :param state: the state for which to get the next states
        :return: a list with all legal next states
        """
        # TODO: Please note that the requirement that the prey never moves into the predator from the previous assignments no longer exists.
        raise NotImplementedError