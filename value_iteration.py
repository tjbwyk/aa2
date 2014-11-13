__author__ = 'Fritjof'
import timeit
from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy


def main():
    as014(verbose=True)


def calculate_value(state, field, policy, value, discount_factor):
    """
    the value iteration calculation, see fig. 4.5 on page 96 of Sutton&Barto
    :param state: current state
    :param field: field environment
    :param policy: policy used
    :param value: value of current state
    :param discount_factor: gamma
    :return: the new value of the current state
    """
    for prob, action in policy.get_probability_mapping(state):
        next_values = []
        for next_state in field.get_next_states(state):
            # for next_state in all_states:
            tmp_prob = policy.get_probability(state, next_state, action)
            tmp_rew = field.get_reward(next_state) + discount_factor * value[next_state]
            next_values.append(tmp_prob * tmp_rew)
    return max(next_values)


def as014(verbose=True):
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.policy = RandomPredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)
    # convergence threshold
    change_epsilon = 0.001
    # gamma
    discount_factor = [0.1, 0.5, 0.7, 0.9]
    gamma_iterations = []

    for gamma in discount_factor:
        start = timeit.default_timer()
        # Initialise value array and temp array:
        values = {state: 0.0 for state in field.get_all_states_with_terminal()}
        all_states = field.get_all_states()

        iterations = 0
        go_on = True
        while go_on:
            delta_value = 0
            iterations += 1
            for state in all_states:
                temp_value = values[state]
                values[state] = calculate_value(state, field, predator.policy, values, gamma)
                delta_value = max(delta_value, abs(temp_value - values[state]))
            if delta_value < change_epsilon:
                go_on = False

        if verbose:
            # print values of all states where prey is located at (5,5)
            for state, value in values.iteritems():
                    if state[1] == (5, 5):
                        print "state: " + str(state) + " value: " + str(value)
        gamma_iterations.append(iterations)
        print "Gamma = " + str(gamma) + " took " + str(iterations) + " iterations and " + str(timeit.default_timer() - start) + " seconds to converge."


if __name__ == '__main__':
    main()
