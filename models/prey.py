from models.player import Player


class Prey(Player):
    """
    The prey class
    """

    def __init__(self, id, location):
        super(Prey, self).__init__(id=id, location=location, tripping_prob=0.2)

    def __str__(self):
        return "Prey" + self.id

    def __hash__(self):
        return hash(self.id)
