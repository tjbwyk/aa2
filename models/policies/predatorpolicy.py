from models.policies.policy import Policy
from models.prey import Prey
import itertools

class PredatorPolicy(Policy, object):
    """
      implementaion of the policy of the predator
    """

    def __init__(self, agent, field):
        super(PredatorPolicy, self).__init__(agent, field)
        self.fixedActions = [(0.8, (0, 0)), (0.05, (0, -1)), (0.05, (-1, 0)), (0.05, (0, 1)), (0.05, (1, 0))]

    def getNextPositions(self, location = self.agent.location):
        return [(prob, self.field.get_new_coordinates(location, fixedAction)) for prob, fixedAction in
               self.fixedActions]

    def getNextStates(self):
        """
        returns the mapping of the next possible states and probabilities
        :param field:
        :param agent: owner of the policy
        :return: all probabilities and according next states
        """

        # TODO: generalize for multiple agents
        prey = self.field.get_players_of_class(Prey)[0] # Take the first prey (assuming only 1)

        # get all potential positions for self and prey
        new_preditor_positions = self.getNextPositionsNoProb()
        new_prey_positions = prey.policy.getNextPositionsNoProb()

        states = [
            (self.field.flatten_index(pred_pos), self.field.flatten_index(prey_pos))
            for pred_pos in new_preditor_positions
                for prey_pos in new_prey_positions
                    if not pred_pos == prey.location
        ]

        return states


    def get_prob_from_state(self, state, action):
        #TODO multiagent style
        for prob, act in self.fixedActions:
            if (action == act):
                return prob


    def getReward(self, action):
      prey = self.field.get_players_of_class(Prey)
      newState = self.field.get_new_coordinates(self.agent.location, action)
      if(prey.location == newState):
        return 10
      else:
        return 0
