from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy


def calculate_value(state, field, policy, value, discount_factor):
    new_value = 0
    for prob, action in policy.get_probability_mapping(state):
        tmp_v = 0
        for next_state in field.get_next_states(state):
            # for next_state in all_states:
            tmp_prob = policy.get_probability(state, next_state, action)
            tmp_rew = field.get_reward(next_state) + discount_factor * value[next_state]
            tmp_v += tmp_prob * tmp_rew
        new_value += prob * tmp_v
    return new_value


def iterative_policy_evaluation(field, discount_factor, all_states, change_epsilon=0.001):
    # Initialise value array and temp array:
    policy = field.get_predator().policy
    value = policy.value

    iterations = 0
    go_on = True
    while go_on:
        delta_value = 0
        iterations += 1
        for state in all_states:
            temp_value = value[state]
            value[state] = calculate_value(state, field, policy, value, discount_factor)
            delta_value = max(delta_value, abs(temp_value - value[state]))
        if delta_value < change_epsilon:
            go_on = False
    print "IPE Iterations: ", iterations
    return value


def init_environment():
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.policy = RandomPredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)
    return field


def calculate_argmax(state, field, policy, value, discount_factor):
    action = policy.pick_next_action(state, style="greedy")
    tmp_v = 0
    for next_state in field.get_next_states(state):
        tmp_prob = policy.get_probability(state, next_state, action)
        tmp_rew = field.get_reward(next_state) + discount_factor * value[next_state]
        tmp_v += tmp_prob * tmp_rew
    return tmp_v


def policy_improvement(field, value, discount_factor, all_states):
    policy = field.get_predator().policy
    policy_stable = True
    for state in all_states:
        # print "Calculate state: ", state
        b = policy.value[state]
        policy.value[state] = calculate_argmax(state, field, policy, value, discount_factor)
        if b != policy.value[state]:
            policy_stable = False
    return policy_stable


def run_policy_iteration(verbose=True):
    field = init_environment()
    # calc once, since all states are always the same
    all_states = field.get_all_states()
    discount_factor = 0.1
    iterations = 0
    end_loop = False

    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    while not end_loop:
        iterations += 1
        print "Starting iteration: ", iterations
        value = iterative_policy_evaluation(field, discount_factor, all_states)
        print "Starting policy improvement"
        end_loop = policy_improvement(field, value, discount_factor, all_states)
        pp.pprint(field.get_predator().policy.value[((5, 5), (6, 7))])

    print "Total Iterations: ", iterations


if __name__ == '__main__':
    run_policy_iteration(verbose=False)
