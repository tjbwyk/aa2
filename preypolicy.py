class PreyPolicy(Policy):
    """
    implementation of the policy of the prey
  """
    def __init__(self):
        self.fixedActions = [(0.8, (0, 0))]
        self.flexActions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    def updatePolicy(self, field, agent):
        """
        updates the prey policy
        :param field:
        :param agent: owner of the policy
        :return: all probabilities and according next states
        """
        newStates = []

        probability = 1
        for fixed in self.fixedActions:
            prob, action = fixed
            probability -= prob

        for flex in self.flexActions:
            newStates.append(field.get_new_coordinates(agent.location, flex))

        for agent in field.getPredators():
            newStates.remove(agent.location)

        flexProb = probability / len(newStates)

        allStates = [(flexProb, x) for x in newStates]
        allStates.extend(self.fixedActions)

        return allStates
