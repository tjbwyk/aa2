from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy
from graphics.gui import GameFrame
from graphics.plot import action_value_quiver_relative
import collections
import time

def calculate_q_value_percentage(field,q_value):
    count = 0
    all_states = field.get_all_states()
    for state in all_states:
        max_action,_ = max_action_for_q(q_value, state, field.get_predator())
        best_actions = field.get_best_actions(state)
        if max_action in best_actions:
            count += 1
    return float(count) /  float(len(all_states))

def max_action_for_q(Q_value, state, predator):
    max = 0
    max_action = (0,0)
    for action in predator.get_actions():
        tmp = Q_value[state, action]
        if tmp > max:
            max = tmp
            max_action = action

    return max_action,max

def compute_q_value(Q_value, old_state, old_action, new_action, reward, new_state, predator, learning_rate=0.1, discount_factor=0.9):

    result = Q_value[old_state, old_action] + \
             learning_rate * (
                 reward +
                 discount_factor * Q_value[new_state,new_action] -
                 Q_value[old_state, old_action]
             )
    return result

def run(learning_rate=0.1, discount_factor=0.9, epsilon=0.1, tau=0.1, value_init=15, num_episodes=1000, verbose=True,policy_style="q-egreedy",
                   gui=False, plot=False):
    """
    Run multiple Q-Learning episodes
    :param learning_rate: the learning rate (alpha)
    :param discount_factor: the discount factor (gamma)
    :param epsilon: the convergence threshold
    :param value_init:
    :param num_episodes:
    :param verbose:
    :param gui: if True, show the game in a GUI
    :param plot: if True, create action-value-plot for the last episode where the prey sits at (5,5)
    :return:
    """
    # Initialize env:
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.policy = RandomPredatorPolicy(predator, field, value_init=value_init)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)

    # set GUI
    if gui:
        GUI = GameFrame(field=field)

    episode_runs = []
    percentage_correct = []
    for i in range(1, num_episodes):
        # Initialize S
        predator.location = (0, 0)
        chip.location = (5, 5)
        old_state = field.get_current_state()
        # Choose A from S using policy derived from Q (e.g., e-greedy)
        old_action = predator.policy.pick_next_action(old_state,style=policy_style, epsilon=epsilon,tau=tau)
        if gui:
            GUI.draw_state(field.get_current_state_complete())
        steps = 0
        while not field.is_ended():
            # Take action A, observe R, S'
            _, prey_action, reward = field.act_with_action(old_action)
            new_state = field.get_current_state()
            # Choose A' from S' using policy derived from Q (e.g., e-greedy)
            new_action = predator.policy.pick_next_action(new_state,style=policy_style, epsilon=epsilon,tau=tau)

            # Q(S, A) <- Q(S, A) + a[R + yQ(S', A') - Q(S, A)]
            predator.policy.q_value[old_state, old_action] = compute_q_value(field.get_predator().policy.q_value, old_state, old_action, new_action, reward, new_state, predator, learning_rate, discount_factor)

            # S <- S'; A <- A';
            old_state = new_state
            old_action = new_action
            if gui:
                GUI.update()
                time.sleep(0.02)
            steps += 1
        episode_runs.append(steps)
        if (i-1) % ((num_episodes) / 300) == 0:
            percentage_correct.append(calculate_q_value_percentage(field,predator.policy.q_value))
        else:
            percentage_correct.append(percentage_correct[-1])
        if verbose:
            if i % (num_episodes / 10) == 0:
                print i,
    print
    if plot:
        #action_values_relative(q_value, relative_state=(-3, 3), path="qlearning_values.pdf")
        title = "Relative actions after " + str(num_episodes) + " episodes of Q-Learning"
        action_value_quiver_relative(predator.policy.q_value, path="sarsa_arrows.pdf", title=title)
    return episode_runs, predator.policy.q_value, percentage_correct


if __name__ == '__main__':
    run(verbose=True, gui=True, plot=True, num_episodes=10000)
    print "Done."
