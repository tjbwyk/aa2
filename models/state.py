class State(object):
    """
    Represents a state
    Responsibilities:
    - Compute terminal states
    """

    def __init__(self, ):
        raise NotImplementedError

    def is_terminal(self):
        return self.predators_have_collided() or self.prey_is_caught()

    def predators_have_collided(self):
        raise NotImplementedError

    def prey_is_caught(self):
        raise NotImplementedError