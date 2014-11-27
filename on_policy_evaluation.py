__author__ = 'sebastian_droeppelmann'
"""
On Policy Monte-Carlo Control
"""
import numpy as np
import models.field


def on_policy_montecarlo(discount_factor=0.7):
    returns_list = []

    field = models.field.init_default_environment()
    field.pick_random_start()
    # play one episode and add visited states to Q-value list
    while not field.is_ended():
        pred_act, prey_act, reward = field.act()
        state = field.get_current_state()
        returns_list.append((state, pred_act))

    first_visit(returns_list, discount_factor, field.get_predator().policy, reward)
    fill_policy(returns_list, field.get_predator().policy, reward)


def fill_policy(sa_list, policy, epsilon):
    """
    after each episode, for each visited state find the optimal action according to maximal Q-values.
    :param sa_list:
    :param policy:
    :param epsilon:
    :return:
    """
    states = set(s for s, a in sa_list)
    for state in states:
        q_list = policy.return_q_values(state)
        tmp_act = None
        tmp_y = -np.inf
        for x, y in q_list:
            if y > tmp_y:
                tmp_act = x
                tmp_y = y

        update_prob_mapping = [(epsilon / len(q_list), act) for act in policy.agent.get_actions()]
        update_prob_mapping.append(((1 - epsilon + epsilon / len(q_list)), tmp_act))
        policy.prob_mapping[state] = update_prob_mapping

        update_prob_mapping = [(epsilon/len(q_list), act) for act in policy.agent.get_actions()]
        update_prob_mapping.append(((1-epsilon+epsilon/len(q_list)), tmp_act))
        policy.prob_mapping[state] = update_prob_mapping

def first_visit(sa_orig_list, discount_factor, policy, reward):
    i = 0
    returns_final = []
    returns_value = []
    sa_list = list(sa_orig_list)

    while len(sa_list) > 0:
        sa = sa_list.pop()
        if sa not in returns_final:
            returns_final.append(sa)
            returns_value.append(discount_factor ** i * reward)
            state, action = sa
            policy.q_value[state, action] = np.average(returns_value)


if __name__ == '__main__':
    on_policy_montecarlo()
    print "Done."

