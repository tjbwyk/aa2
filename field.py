__author__ = 'fbuettner'

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

    def add_player(self, player):
        player.field = self
        self.players.append(player)

    def get_players_of_class(self, player_class):
        result = []
        for player in self.players:
            if isinstance(player, player_class):
                result.append(player)
        return result

    def __str__(self):
        result = ""
        for player in self.players:
            result += player.name + "(" + player.location[0] + "," + player.location[1] + "), "
        return result

    def print_field(self):

        # first line
        res = "-" + "--"*self.width + "\n"
        for row in range(self.height):
            res += "|"