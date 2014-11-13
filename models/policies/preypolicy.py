from models.policies.policy import Policy

class PreyPolicy(Policy, object):
    """
    implementation of the policy of the prey
    """

    def __init__(self, agent, field, seed=None):
        super(PreyPolicy, self).__init__(agent, field, seed=seed)