__author__ = 'sebastian_droeppelmann'
"""
On Policy Monte-Carlo Control
"""
import numpy as np
import models.field
import time
from graphics.gui import GameFrame

def run_on_policy_montecarlo(num_episodes=100, discount_factor=0.7, verbose=False, gui=False):
    """
    wrapper function to simulate multiple episodes of on-policy MC control.
    :param num_episodes: how many episodes
    :param discount_factor: gamma
    :param verbose: if True: print progress (every 10%) to console
    :param gui: if True: run on episode with the learned policy in the gui.
    :return:
    """
    environment = models.field.init_default_environment()
    for i in xrange(num_episodes):
        on_policy_montecarlo(environment, discount_factor)
        if verbose and i % (num_episodes / 10) == 0:
            print i
    if gui:
        GUI = GameFrame(field=environment)
        time.sleep(1)
        environment.pick_random_start()
        GUI.update(trace=False)
        while not environment.is_ended():
            environment.act()
            GUI.update()
            time.sleep(0.1)



def on_policy_montecarlo(field, discount_factor=0.7):
    """
    Generate one episode of on-policy MC control
    :param discount_factor: gamma
    :return:
    """
    # returns for visited state-action pairs in this episode
    returns_list = []
    # pick a random start state
    field.pick_random_start()
    # play one episode and add visited states to Q-value list
    while not field.is_ended():
        pred_act, prey_act, reward = field.act()
        state = field.get_current_state()
        returns_list.append((state, pred_act))
    # calculate first-visit Q-values
    first_visit(returns_list, discount_factor, field.get_predator().policy, reward)
    # update policy
    fill_policy(returns_list, field.get_predator().policy, reward)


def fill_policy(sa_list, policy, epsilon):
    """
    after each episode, for each visited state find the optimal action according to maximal Q-values.
    :param sa_list: history of the states and actions in that episode
    :param policy: the policy object
    :param epsilon: the epsilon-soft policy parameter
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
        # for all possible actions in state s, compute the probabilities:
        # epsilon / number of possible actions for all non-optimal actions
        update_prob_mapping = [(epsilon / len(q_list), act) for act in policy.agent.get_actions()]
        # 1 - epsilon + epsilon / number of possible actions for the optimal action
        update_prob_mapping.append(((1 - epsilon + epsilon / len(q_list)), tmp_act))
        policy.prob_mapping[state] = update_prob_mapping


def first_visit(sa_orig_list, discount_factor, policy, reward):
    """
    For each state-action pair that appeared in the episode, add the return value of the first occurrence of this pair
    in this episode to the list of returns for this state-action pair (for all episodes). Then compute the Q-Value
    as the average of all returns.
    :param sa_orig_list:
    :param discount_factor:
    :param policy:
    :param reward:
    :return:
    """
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
    run_on_policy_montecarlo(num_episodes=10, discount_factor=0.9, verbose=True, gui=True)
    print "Done."

