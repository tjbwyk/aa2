import numpy as np
from models.predator import Predator
from models.prey import Prey


class Field(object):
    """
    Models the environment:
    Responsibilities:
    - Maintaining a list of agents
    -
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
        """
        Returns the new location given the current location and a movement delta
        :param current_location: the current location on the field
        :param delta: the movement delta
        :return:the new location on the field
        """
        (x, y) = current_location
        (delta_x, delta_y) = delta
        new_location = (
            (x + delta_x) % self.width,
            (y + delta_y) % self.height
        )
        return new_location

    def get_relative_position(self, location1, location2):
        """
        returns the relative position of location1 according to location2
        :param location1: the first location
        :param location2: the second location
        :return: relative position
        """
        x1, y1 = location1
        move = ((int(np.floor(self.width / 2)) - x1), (int(np.floor(self.height / 2)) - y1))
        x1, y1 = self.get_new_coordinates(location1, move)
        x2, y2 = self.get_new_coordinates(location2, move)
        return (x2 - x1), (y2 - y1)

    def add_player(self, player):
        """
        adds a player to the field
        :param player: the player to add
        """
        self.players.append(player)

    def get_players(self, exception_player=None):
        """
        returns all players except for the exception player
        :param exception_player: the player not to include in the list
        :return: a list with players
        """
        return [player for player in self.players if player is not exception_player]

    def get_players_of_class(self, player_class, exception_player=None):
        """
        return all players of a certain class except for the exception player
        :param player_class: the class of which the players should be from
        :param exception_player: the player not to include
        :return: a list with players
        """
        return [player for player in self.players if
                isinstance(player, player_class) and player is not exception_player]

    def get_predators(self, exception_player=None):
        """
        returns all players of classtype predator except for the exception player
        :param exception_player: the player not to include
        :return: a list of predators
        """
        return self.get_players_of_class(Predator, exception_player)

    def get_prey(self):
        """
        returns the player of classtype prey
        :return: the prey
        """
        return self.get_players_of_class(Prey)[0]

    def is_ended(self):
        """
        returns if the episode is ended
        :return: true if terminal state is reached
        """
        return self.state.is_terminal()

    def get_reward(self, state=None):
        """
        returns a reward for the current state given
        :param state:
        :return:
        """
        raise NotImplementedError

    def get_current_state(self):
        """
        returns the current state representation of the field
        :return: the current state
        """
        return self.state