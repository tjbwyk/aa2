from models.player import Player


class Predator(Player):
    """
    The predator class
    """

    def __init__(self, location):
        super(Predator, self).__init__(location)

    def __str__(self):
        return "Predator"

    def get_next_locations(self):
        return [self.field.get_new_coordinates(self.location, action) for action in self.actions]

    def act(self):
        act, preyact = self.policy.pick_next_action()
        self.location = self.field.get_new_coordinates(self.location, act)
        self.field.update_prey_location(preyact)