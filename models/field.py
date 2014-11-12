from models.predator import Predator
from models.prey import Prey
import itertools
import numpy as np


class Field(object):
    """
    the playground
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []

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
        move = ((x1 - int(np.floor(self.width/2))), (y1 - int(np.floor(self.height/2))))
        x1, y1 = self.get_new_coordinates(location1, move)
        x2, y2 = self.get_new_coordinates(location2, move)
        return (x2-x1), (y2-y1)

    def add_player(self, player):
        player.field = self
        self.players.append(player)

    def get_players_of_class(self, player_class, exception_player=None):
        return [ player for player in self.players if isinstance(player, player_class) and player is not exception_player]

    def get_predators(self, exception_player=None):
        return self.get_players_of_class(Predator, exception_player)

    def get_preys(self, exception_player=None):
        return self.get_players_of_class(Prey, exception_player)

    def get_players(self, exception_player=None):
        return [player for player in self.players if player is not exception_player]

    def __str__(self):
        result = map(lambda p: str(p) + "(" + str(p.location[0]) + "," + str(p.location[1]) + ")", self.players)
        return ", ".join(result)

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
        if state == (0, 0):
            return 10
        else:
            return 0

    def update_prey_location(self, preyact):
        self.get_preys()[0].location = self.get_new_coordinates(self.get_preys()[0].location, preyact)


    # def get_state(self):
    #     state = ()
    #     for player in self.players:
    #         state = state + (self.flatten_index(player.location),)
    #     return state
    #
    # # State representations
    # def state_iterator(self):
    #     return itertools.product(range(self.height*self.width),repeat=len(self.players))

    # def flatten_index(self,(x,y)):
    #     return np.ravel_multi_index((x,y),(self.width,self.height))
    #
    # def unflatten_index(self,index):
    #     return np.unravel_index(index,(self.width,self.height))
