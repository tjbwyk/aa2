from models.policies.policy import Policy
from models.predator import Predator


class PreyPolicy(Policy, object):
    """
    implementation of the policy of the prey
    """

    def __init__(self, agent, field):
        super(PreyPolicy, self).__init__(agent, field)
        self.fixedActions = [(0.8, (0, 0))]
        self.flexActions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    def getNextStates(self):
        """
        updates the prey policy
        :param field:
        :param agent: owner of the policy
        :return: all probabilities and according next states
        """
        flexStates = [self.field.get_new_coordinates(self.agent.location, flexAction) for flexAction in
                      self.flexActions]

        fixedStates = []
        probability = float(1)

        for prob, fixedAction in self.fixedActions:
            fixedStates.append((prob, self.field.get_new_coordinates(self.agent.location, fixedAction)))
            probability -= prob

        for agent in self.field.get_players_of_class(Predator):
            if agent.location in flexStates:
                flexStates.remove(agent.location)

        flexProb = probability / len(flexStates)
        nextStates = [(flexProb, flexState) for flexState in flexStates]
        nextStates.extend(fixedStates)
        return nextStates
