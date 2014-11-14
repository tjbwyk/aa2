from models.field import Field
from models.predator import Predator
from models.prey import Prey
#from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.predatorpolicy import PredatorPolicy
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
    predator.policy = PredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)
    return field

def calculate_argmax(state, field, policy, discount_factor):
    action_value = 0
    for action in policy.agent.get_actions():
        tmp_v = 0
        for next_state in field.get_next_states(state, action):
            tmp_prob = policy.get_probability(state, next_state, action)
            tmp_rew = field.get_reward(next_state) + discount_factor * policy.value[next_state]
            tmp_v += tmp_prob * tmp_rew
        if tmp_v > action_value:
            sel_act = action
            action_value = tmp_v
    return sel_act

def policy_improvement(field, discount_factor, all_states):
    policy = field.get_predator().policy
    policy_stable = True
    for state in all_states:
        #print "Calculate state: ", state
        b = policy.argmax_action[state]
        policy.argmax_action[state] = calculate_argmax(state, field, policy, discount_factor)
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


def run_policy_iteration(verbose=True, plot_values=False):
    if verbose:
        print "=== POLICY ITERATION ==="
    field = init_environment()
    # calc once, since all states are always the same
    all_states = field.get_all_states()

    # convergence threshold
    change_epsilon = 0.00001
    # gamma
    discount_factor = [0.1, 0.5, 0.7, 0.9]
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
            pandas.DataFrame(print_values).to_csv(path_or_buf="reports/policyiteration_gamma"+str(gamma)+".csv", sep=";")
            if plot_values:
                plot.value_heatmap(print_values, path="reports/policyiteration_gamma"+str(gamma)+".pdf")
        print "Gamma = " + str(gamma) + " took " + str(iterations) + " iterations and " + str(timeit.default_timer() - start) + " seconds to converge."

if __name__ == '__main__':
    run_policy_iteration(verbose=True, plot_values=True)