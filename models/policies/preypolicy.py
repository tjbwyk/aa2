from models.policies.policy import Policy
from models.predator import Predator


class PreyPolicy(Policy, object):
    """
    implementation of the policy of the prey
    """

    def __init__(self, agent, field, seed=None):
        super(PreyPolicy, self).__init__(agent, field,
        fixed_actions = [(0.8, (0, 0))],
        flex_actions = [(0, -1), (-1, 0), (0, 1), (1, 0)], seed=seed)

    def get_probability_mapping(self):
        """
        updates the prey policy
        :param field:
        :param agent: owner of the policy
        :return: all probabilities and according next states
        """
        flex_states = [self.field.get_new_coordinates(self.agent.location, flexAction)
                       for flexAction in self.flex_actions]
        fixed_states = []
        probability = 1.0

        for prob, fixedAction in self.fixed_actions:
            fixed_states.append((prob, self.field.get_new_coordinates(self.agent.location, fixedAction)))
            probability -= prob

        for agent in self.field.get_predators():
            if agent.location in flex_states:
                flex_states.remove(agent.location)

        flexProb = probability / len(flex_states)
        nextStates = [(flexProb, flexState) for flexState in flex_states]
        nextStates.extend(fixed_states)
        return nextStates
