from player import Player


class Predator(Player):
    """
    The predator class
    """
    def __init__(self, location):
        super(Predator, self).__init__(location)

    def __str__(self):
        return "Predator"
