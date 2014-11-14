__author__ = 'Fritjof'
import timeit

import numpy as np
import pandas

from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.predatorpolicy import PredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy
from graphics import plot


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
    next_states = field.get_next_states(state)
    next_values = []
    # Loop over all actions
    for action in policy.agent.get_actions():
        tmp_ns = []
        cur_pred_pos, cur_prey_pos = state
        # Get the next location resulting from this action
        next_loc = field.get_new_coordinates(cur_pred_pos, action)

        # Select all next states for which the predator end up in this location
        for ns in next_states:
            if ns[0] == next_loc:
                tmp_ns.append(ns)

        # Using only the states that we actually end up in for this action, calculate the value of that action
        for next_state in tmp_ns:
            # for next_state in all_states:
            tmp_prob = policy.get_probability(state, next_state, action)
            tmp_rew = field.get_reward(next_state) + discount_factor * value[next_state]
            next_values.append(tmp_prob * tmp_rew)
    # The value of this state is the highest value possible
    return max(next_values)


def run_value_iteration(verbose=True, plot_values=False):
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.policy = PredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)
    # convergence threshold
    change_epsilon = 0.00001
    # gamma
    discount_factor = [0.1, 0.5, 0.7, 0.9]
    # discount_factor = [0.9]
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
            print_values = np.zeros((field.height, field.width))
            for state, value in values.iteritems():
                if state[1] == (5, 5):
                    #print "  state: " + str(state) + " value: " + str(value)
                    print_values[state[0]] = value
            #input("Press enter to continue")
            # convert to pandas DF for pretty print and save to CSV file in reports directory
            out_path = "reports/valueiteration_gamma" + str(gamma).replace(".", "-")
            pandas.DataFrame(print_values).to_csv(path_or_buf=out_path + ".csv", sep=";")
            if plot_values:
                plot.value_heatmap(print_values, path=out_path + ".pdf")
        gamma_iterations.append(iterations)
        print "Gamma = " + str(gamma) + " took " + str(iterations) + " iterations and " + str(
            timeit.default_timer() - start) + " seconds to converge."


if __name__ == '__main__':
    run_value_iteration(verbose=True, plot_values=True)
    print "Done."
