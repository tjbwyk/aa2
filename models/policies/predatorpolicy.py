from models.policies.policy import Policy


class PredatorPolicy(Policy, object):
    """
      implementaion of the policy of the predator
    """

    def __init__(self, agent, field):
        super(PredatorPolicy, self).__init__(agent, field)
        self.fixedActions = [(0.8, (0, 0)), (0.05, (0, -1)), (0.05, (-1, 0)), (0.05, (0, 1)), (0.05, (1, 0))]

    def getNextStates(self):
        """
        returns the mapping of the next possible states and probabilities
        :param field:
        :param agent: owner of the policy
        :return: all probabilities and according next states
        """
        fixedStates = [(prob, self.field.get_new_coordinates(self.agent.location, fixedAction)) for prob, fixedAction in
                       self.fixedActions]
        return fixedStates
