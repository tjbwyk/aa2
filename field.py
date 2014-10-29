__author__ = 'fbuettner'

class Field(object):
    """
    the playground
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.players = []

    def get_new_coordinates(self, current_x, current_y, delta_x, delta_y):
        new_x = (current_x + delta_x) % self.width
        new_y = (current_y + delta_y) % self.height

        return new_x, new_y

    def add_player(self, player):
        player.field = self
        self.players.append(player)

    def __str__(self):
        result = ""
        for player in self.players:
            result += player.name + "(" + player.x + "," + player.y + "), "
        return result