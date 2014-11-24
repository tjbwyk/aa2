from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy
from iterative_policy_evaluation import iterative_policy_evaluation
import timeit
import numpy as np
import pandas
from graphics import plot


def init_environment():
    field = Field(11, 11)
    predator = Predator((0, 0))
#    predator.policy = RandomPredatorPolicy(predator, field)
    predator.policy = RandomPredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)
    return field


def policy_improvement(field, discount_factor, all_states):
    policy = field.get_predator().policy
    policy_stable = True
    for state in all_states:
        #print "Calculate state: ", state
        b = policy.argmax_action[state]
        # update best action for this state
        policy.argmax_action[state] = policy.pick_next_action(state=state, style="max_value", gamma=discount_factor)
        if b != policy.argmax_action[state]:
            policy_stable = False
    return policy_stable


def policy_iteration(field, discount_factor, all_states, change_epsilon):
    end_loop = False
    iterations = 0
    while not end_loop:
        iterations += 1
        #print "Starting iteration: ", iterations
        iterative_policy_evaluation(field, discount_factor, all_states, change_epsilon)
        #print "Starting policy improvement"
        end_loop = policy_improvement(field, discount_factor, all_states)
    return iterations


def run_policy_iteration(verbose=True, plot_values=False, discount_factor=[0.1, 0.5, 0.7, 0.9], change_epsilon=0.00001):
    """
    run the game using policy
    :param verbose: if set to true, will print the states where the prey sits at (5,5) and the according values.
    :param plot_values: if set to true, will plot a heatmap of the values where the prey sits at (5,5) and save it to a
                            PDF file in the reports/ subfolder.
    :param discount_factor: a list of discount factors (gamma) to iterate over. default: [0.1, 0.5, 0.7, 0.9]
    :param change_epsilon: convergence condition for iterative policy evaluation. Will stop when changes are smaller.
    :return: None
    """
    if verbose:
        print "=== POLICY ITERATION ==="
    field = init_environment()
    # calc once, since all states are always the same
    all_states = field.get_all_states()

    # convergence threshold

    # gamma

    gamma_iterations = []

    for gamma in discount_factor:
        start = timeit.default_timer()

        field.get_predator().policy.reset_planning()
        iterations = policy_iteration(field, gamma, all_states, change_epsilon)
        gamma_iterations.append(iterations)

        if verbose:
            # print values of all states where prey is located at (5,5)
            print_values = np.zeros((field.height, field.width))
            for state, value in field.get_predator().policy.value.iteritems():
                if state[1] == (5, 5):
                    print_values[state[0]] = value

            # convert to pandas DF for pretty print and save to CSV file in reports directory
            pandas.DataFrame(print_values).to_csv(path_or_buf="reports/policyiteration_gamma" + str(gamma) + ".csv",
                                                  sep=";")
            if plot_values:
                plot.value_heatmap(print_values, path="reports/policyiteration_gamma" + str(gamma) + ".pdf")
        print "Gamma = " + str(gamma) + " took " + str(iterations) + " iterations and " + str(
            round(timeit.default_timer() - start, 2)) + " seconds to converge."
    return None


if __name__ == '__main__':
    run_policy_iteration(verbose=True, plot_values=True)
