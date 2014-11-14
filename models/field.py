import numpy as np

from models.predator import Predator
from models.prey import Prey


class Field(object):
    """
    the playground
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []

    def __str__(self):
        result = map(lambda p: str(p) + "(" + str(p.location[0]) + "," + str(p.location[1]) + ")", self.players)
        return ", ".join(result)

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


    def get_distance(self, state):
        pred_pos, prey_pos = state
        x, y = self.get_relative_position(pred_pos, prey_pos)
        return abs(x) + abs(y)

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

    def get_predator(self):
        return self.get_predators()[0]

    def get_prey(self):
        return self.get_preys()[0]

    def print_field(self):
        predators = [predator.location for predator in self.get_players_of_class(Predator)]
        preys = [prey.location for prey in self.get_players_of_class(Prey)]
        res = ""
        for row in range(self.height):
            res += "|"
            for col in range(self.width):
                if (col, row) in predators:
                    res += "X"
                elif (col, row) in preys:
                    res += "O"
                else:
                    res += " "
                res += "|"
            res += "\n"
        return res

    def is_ended(self):
        """
        checks if all preys have been found by a predator
        :return: true if game is over
        """
        predators = self.get_predators()
        preys = self.get_preys()

        found_all = True
        for prey in preys:
            found_prey = False
            for predator in predators:
                if prey.location == predator.location:
                    found_prey = True
            found_all &= found_prey
        return found_all

    def get_reward(self, state):
        """
        returns a reward for the current state given
        :param state:
        :return:
        """
        pred_loc, prey_loc = state
        if pred_loc == prey_loc:
            return 10
        else:
            return 0

    def get_all_states_with_terminal(self):
        """
        returns all states except for the terminal states: S
        :return: list of all states except the terminal ones
        """
        return set([((x, y), (i, j))
                    for x in range(self.height) for y in range(self.width)
                    for i in range(self.height) for j in range(self.width)])

    def get_all_states(self):
        """
        returns all states except for the terminal states: S
        :return: list of all states except the terminal ones
        """
        return set([((x, y), (i, j))
                    for x in range(self.height) for y in range(self.width)
                    for i in range(self.height) for j in range(self.width)
                    if not (x == i and y == j)])


    def get_current_state(self):
        """
        returns the current state of the environment
        :return: the current state
        """
        # state = ()
        # for player in self.players:
        # state = state + (player.location,)
        # return state
        return (self.get_predator().location, self.get_prey().location)

    def get_next_states(self, state):
        """
        returns all next states from the given state that are not illegal
        :param state: the state for which to get the next states
        :return: a list with all legal next states
        """
        cur_pred_pos, cur_prey_pos = state
        next_pred_positions = self.get_predator().get_next_locations(state)
        next_prey_positions = self.get_prey().get_next_locations(state)
        # initialize all next possible states except when the predator moves t the prey
        next_states = [(next_pred_pos, next_prey_pos)
                       for next_pred_pos in next_pred_positions
                       for next_prey_pos in next_prey_positions
                       if cur_prey_pos != next_pred_pos]

        #if predator moves to the prey, the prey always stays where it is
        #and the predator is on top of it, this has to be added since we filtered all movements with
        #this situation earlier
        if cur_prey_pos in next_pred_positions:
            next_states.append(((cur_prey_pos), (cur_prey_pos)))

        return next_states