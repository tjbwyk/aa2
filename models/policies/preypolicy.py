from models.policies.policy import Policy
from models.predator import Predator


class PreyPolicy(Policy, object):
    """
    implementation of the policy of the prey
    """

    def __init__(self, agent, field, seed=None):
        super(PreyPolicy, self).__init__(agent, field,
                                         fixed_actions=[(0.8, (0, 0))],
                                         flex_actions=[(0, -1), (-1, 0), (0, 1), (1, 0)], seed=seed)

    def get_next_locations(self, location=None):
        """
        updates the prey policy
        :param location:
        :return: all probabilities and according next states
        """
        if location is None:
            location = self.agent.location

        flex_states = [(flex_action, self.field.get_new_coordinates(location, flex_action))
                       for flex_action in self.flex_actions]
        fixed_states = []
        probability = 1.0

        for prob, fixed_action in self.fixed_actions:
            fixed_states.append((prob, fixed_action, self.field.get_new_coordinates(location, fixed_action)))
            probability -= prob

        for agent in self.field.get_predators():
            for act, loc in flex_states:
                if agent.location == loc:
                    flex_states.remove((act, loc))

        flex_prob = probability / len(flex_states)
        next_states = [(flex_prob, act, flex_state) for act, flex_state in flex_states]
        next_states.extend(fixed_states)
        return next_states
