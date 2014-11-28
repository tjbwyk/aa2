__author__ = 'sebastian_droeppelmann'
"""
On Policy Monte-Carlo Control
"""
import numpy as np
import models.field
import time
from graphics.gui import GameFrame


def run_on_policy_montecarlo(num_episodes=1000, discount_factor=0.7, verbose=False, gui=False):
    """
    wrapper function to simulate multiple episodes of on-policy MC control.
    :param num_episodes: how many episodes
    :param discount_factor: gamma
    :param verbose: if True: print progress (every 10%) to console
    :param gui: if True: run on episode with the learned policy in the gui.
    :return:
    """
    environment = models.field.init_default_environment()
    nr_steps = []
    for i in xrange(1, num_episodes + 1):
        steps = on_policy_montecarlo(environment, i)
        nr_steps.append(steps)

        if verbose and ((num_episodes > 10 and i % (num_episodes / 10) == 0) or num_episodes <= 10):
            print i, "Runs, average Steps: ", np.average(nr_steps[i - (num_episodes / 10):i])
            print environment.get_predator().policy.return_q_values((-1, 0))
            print [(environment.get_predator().policy.q_value[(0, -1), action], action) for action in
                   environment.get_predator().get_actions()]
            print [(environment.get_predator().policy.q_value[(0, -1), action], action) for action in
                   environment.get_predator().get_actions()]
            print [(environment.get_predator().policy.q_value[(0, -1), action], action) for action in
                   environment.get_predator().get_actions()]
            print "Q", environment.get_predator().policy.q_value
            print "R", environment.get_predator().policy.returns
            print "P", environment.get_predator().policy.prob_mapping

    print "Q", environment.get_predator().policy.q_value
    print "R", environment.get_predator().policy.returns
    print "P", environment.get_predator().policy.prob_mapping

    print environment.get_predator().policy.return_q_values((0, -1))

    if gui:
        GUI = GameFrame(field=environment)
        time.sleep(1)
        environment.pick_random_start()
        GUI.update(trace=False)
        while not environment.is_ended():
            environment.act(style="greedy")
            GUI.update()
            time.sleep(0.1)


def on_policy_montecarlo(field, nr_episodes, epsilon=0.1):
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
    i = 0
    while not field.is_ended():
        i += 1
        pred_act, prey_act, reward = field.act(style="egreedy", epsilon=epsilon)
        state = field.get_current_state()
        returns_list.append((state, pred_act))
    # calculate first-visit Q-values
    first_visit(returns_list, field.get_predator().policy, nr_episodes, reward)
    # update policy
    fill_policy(returns_list, field.get_predator().policy, epsilon)
    return i


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
        for rew, act in q_list:
            if rew > tmp_y:
                tmp_act = act
                tmp_y = rew
        # for all possible actions in state s, compute the probabilities:
        # epsilon / number of possible actions for all non-optimal actions
        update_prob_mapping = [(epsilon / len(q_list), act) for act in policy.agent.get_actions() if act != tmp_act]
        # 1 - epsilon + epsilon / number of possible actions for the optimal action
        update_prob_mapping.append(((1 - epsilon + epsilon / len(q_list)), tmp_act))
        policy.prob_mapping[state] = update_prob_mapping


def first_visit(sa_orig_list, policy, nr_episodes, reward):
    """
    For each state-action pair that appeared in the episode, add the return value of the first occurrence of this pair
    in this episode to the list of returns for this state-action pair (for all episodes). Then compute the Q-Value
    as the average of all returns.
    :param sa_orig_list:
    :param nr_episodes: number of episodes played so far
    :param policy:
    :param reward:
    :return:
    """
    returns_final = []
    sa_list = list(sa_orig_list)
    i = 0
    discount = 0.9
    while len(sa_list) > 0:
        sa = sa_list.pop()
        if sa not in returns_final:
            i += 1
            returns_final.append(sa)
            state, action = sa
            count, value = policy.returns[state, action]
            # value += discount**i*reward
            value += reward
            count += 1
            policy.returns[state, action] = (count, value)
            policy.q_value[state, action] = float(value) / nr_episodes


if __name__ == '__main__':
    run_on_policy_montecarlo(num_episodes=5, verbose=True, gui=True)
    print "Done."

