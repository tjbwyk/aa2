import numpy as np
import random
from models.predator import Predator
from models.prey import Prey
from models.state import State


class Field(object):
    """
    Models the environment:
    Responsibilities:
    - Maintaining a list of agents
    - coordination of the steps in an episode
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []
        self.state = None
        self.steps = 0

    def __str__(self):
        result = map(lambda p: str(p) + "(" + str(p.location[0]) + "," + str(p.location[1]) + ")", self.players)
        return ", ".join(result)

    def run_step(self):
        """
        Runs a step of the current episode by telling all agents to pick their respective next action based on the
        state of the field. Then, it computes the locations of all players in the next state and possible rewards.
        Finally, new state and reward is distributed to all players so they can learn from their action.
        :return:
        """
        old_state = self.state
        actions = dict()
        # for every player:
        for player in self.players:
            # call act() function on player and get desired action in return
            actions[player] = player.act(self.state)
        # compute next state based on actions chosen by players
        for player in self.players:
            player.location = self.transition(player, actions.get(player))
        # update field state
        self.state = State.state_from_field(self)
        # tell each player their new location and reward
        for player in self.players:
            reward = self.get_reward(player)
            player.update(old_state=old_state, new_state=self.state, action=actions[player], reward=reward)
        self.steps += 1
        return

    def transition(self, player, action):
        """
        This function determines what state the desired action of an agent leads to. For example, if the agent has a
        tripping_probability > 0, it may end up in the same state it came from.
        :param player: the player who wants to take the action
        :param action: the desired action
        :return: the new state of the agent
        """
        # tripping?
        if random.random() < player.tripping_prob:
            # player trips, stays on same location
            new_state = player.location
        else:
            # player moves to new location according to action
            new_state = self.get_new_coordinates(player.location, action)
        return new_state

    def get_new_coordinates(self, current_location, delta):
        """
        Returns the new location given the current location and a movement delta (= action)
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
        self.state = State.state_from_field(self)

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

    def get_reward(self, player):
        """
        returns a reward for a specific player in the current state of the field.
        If two or more predators run into each other, they get a reward of -10 and the prey escaped and gets a
        reward of +10. If one predator catches the prey, all predators get a reward of +10 and the prey
        gets a reward of -10. Predator failure prevails over catching the prey.
        :return:
        """
        # predator rewards
        if isinstance(player, Predator):
            if self.state.predators_have_collided():
                return -10
            elif self.state.prey_is_caught():
                return 10
        # prey rewards
        elif isinstance(player, Prey):
            if self.state.predators_have_collided():
                return 10
            elif self.state.prey_is_caught():
                return -10
        # default reward
        return 0

    def get_current_state(self):
        """
        returns the current state representation of the field
        :return: the current state
        """
        return self.state