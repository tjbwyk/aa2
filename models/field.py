import numpy as np
import random

from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy

def init_default_environment(pred_loc=(0, 0), prey_loc=(5, 5), value_init=5):
    field = Field(3, 3)
    field.add_player(Predator(pred_loc))
    field.add_player(Prey(prey_loc))
    field.get_predator().policy = RandomPredatorPolicy(field.get_predator(), field, value_init)
    field.get_prey().policy = RandomPreyPolicy(field.get_prey(), field, value_init)
    return field

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

    def act(self, **kwargs):
        pred_act = self.get_predator().act(**kwargs)
        prey_act = self.get_prey().act()
        reward = self.get_reward()
        return pred_act, prey_act, reward

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

    def get_relative_movement(self, relative_position, action, player="predator"):
        rp_x, rp_y = relative_position
        a_x, a_y = action
        if (player == "predator"):
            tmp_x = rp_x - a_x
            tmp_y = rp_y - a_y
        else:
            tmp_x = rp_x + a_x
            tmp_y = rp_y + a_y

        while (tmp_x) < -1 * int(np.floor(self.width / 2)):
            tmp_x += self.width
        while (tmp_y) < -1 * int(np.floor(self.height / 2)):
            tmp_y += self.height
        while (tmp_x) > int(np.floor(self.width / 2)):
            tmp_x -= self.width
        while (tmp_y) > int(np.floor(self.height / 2)):
            tmp_y -= self.height

        return (tmp_x, tmp_y)

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

    def pick_random_start(self):
        startState = random.sample(self.get_all_states_complete(), 1)
        predPos, preyPos = startState[0]
        self.get_predator().location = predPos
        self.get_prey().location = preyPos


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

    def get_distance(self, state):
        return self.get_distance_relative(state)
        #return self.get_distance_complete(state)

    def get_distance_relative(self, state):
        x, y = state
        return abs(x) + abs(y)

    def get_distance_complete(self, state):
        pred_pos, prey_pos = state
        x, y = self.get_relative_position(pred_pos, prey_pos)
        return abs(x) + abs(y)

    def get_reward(self, state = None):
        """
        returns a reward for the current state given
        :param state:
        :return:
        """
        if state is None:
            state = self.get_current_state()
        return self.get_reward_relative(state)
        #return self.get_reward_complete(state)

    def get_reward_relative(self, state):
        if state == (0,0):
            return 10
        else:
            return 0

    def get_reward_complete(self, state):
        pred_loc, prey_loc = state
        if pred_loc == prey_loc:
            return 10
        else:
            return 0

    def get_all_states_with_terminal(self):
        return self.get_all_states_with_terminal_relative()
        #return self.get_all_states_with_terminal_complete(self)

    def get_all_states_with_terminal_relative(self):
        rel_x_lim = int(np.floor(self.width/2))
        rel_y_lim = int(np.floor(self.height/2))
        return set([(x, y) for x in range(-1* rel_x_lim, rel_x_lim+1) for y in range(-1* rel_y_lim, rel_y_lim+1)])

    def get_all_states_with_terminal_complete(self):
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
        return self.get_all_states_relative()
        #return self.get_all_states_complete()

    def get_all_states_relative(self):
        rel_x_lim = int(np.floor(self.width/2))
        rel_y_lim = int(np.floor(self.height/2))
        return set([(x, y)
                    for x in range(-1 * rel_x_lim, rel_x_lim + 1)
                    for y in range(-1 * rel_y_lim, rel_y_lim + 1)
                    if (x, y) != (0, 0)])

    def get_all_states_complete(self):
        return set([((x, y), (i, j))
                    for x in range(self.height) for y in range(self.width)
                    for i in range(self.height) for j in range(self.width)
                    if not (x == i and y == j)])

    def get_current_state(self):
        """
        returns the current state of the environment
        :return: the current state
        """
        return self.get_current_state_relative()
        #return self.get_current_state_complete()

    def get_current_state_relative(self):
        return self.get_relative_position(self.get_predator().location, self.get_prey().location)

    def get_current_state_complete(self):
        # state = ()
        # for player in self.players:
        # state = state + (player.location,)
        # return state
        return (self.get_predator().location, self.get_prey().location)

    def get_next_states(self, state, pred_action=None):
        """
        returns all next states from the given state that are not illegal
        :param state: the state for which to get the next states
        :return: a list with all legal next states
        """
        return self.get_next_states_relative(state, pred_action)
        #return self.get_next_states_complete(state, pred_action)

    def get_next_states_relative(self, state, pred_action=None):

        if pred_action is None:
            next_pred_positions = [self.get_relative_movement(state, action) for action in self.get_predator().get_actions()]
        else:
            next_pred_positions = [self.get_relative_movement(state, pred_action)]

        prey_actions = self.get_prey().get_actions()

        if self.get_distance(state) == 1:
            x, y = state
            prey_actions.remove((-1*x, -1*y))

        next_prey_positions = [self.get_relative_movement(next_state, action, player="prey")
                               for next_state in next_pred_positions
                               for action in prey_actions
                               if next_state != (0, 0)]

        if (0, 0) in next_pred_positions:
            next_prey_positions.append((0,0))

        return next_prey_positions

    def get_next_states_complete(self, state, pred_action=None):
        cur_pred_pos, cur_prey_pos = state
        if pred_action is None:
            next_pred_positions = self.get_predator().get_next_locations(state)
        else:
            next_pred_positions = [self.get_new_coordinates(cur_pred_pos, pred_action)]

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
