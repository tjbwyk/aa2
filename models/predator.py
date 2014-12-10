from models.player import Player


class Predator(Player):
    """
    The predator class
    """

    def __init__(self, id, location):
        super(Predator, self).__init__(id=id, location=location, tripping_prob=0.0)

    def __str__(self):
        return "Predator" + self.id

    def __hash__(self):
        return hash(self.id)