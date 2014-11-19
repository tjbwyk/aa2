import numpy as np
from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.predatorpolicy import PredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy
import collections
import matplotlib.pyplot as plt

def max_action_value_for_q(Q_value, state, predator):
    max = 0
    for action in predator.get_actions():
        tmp = Q_value[state,action]
        if tmp > max:
            max = tmp

    return max

def compute_q_value(Q_value, cur_state, action, reward, new_state, predator, learning_rate = 0.2, discount_factor = 0.5):
    result = Q_value[cur_state,action] +\
        learning_rate * (
            reward +
            discount_factor*max_action_value_for_q(Q_value,new_state,predator) -
            Q_value[cur_state,action]
        )
    return result

def run_q_learning(verbose=True):
    NUM_EPISODES = 15000

    # Initialize env:
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.policy = PredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)

    # Initialize Q(s,a) optimistically with a value of 15
    q_value = collections.defaultdict(lambda: 15)

    # Set policy
    policy = PredatorPolicy(predator,field,qvalue=q_value)

    episode_runs = []
    for i in range(1,NUM_EPISODES):
        predator.location = (0,0)
        chip.location     = (5,5)
        cur_state = field.get_current_state()
        steps = 0
        while not field.is_ended():
            action = policy.pick_next_action(cur_state, style="q-egreedy",epsilon=0.1)
            field.take_action(action)
            reward = field.get_reward()
            new_state = field.get_current_state()

            q_value[cur_state,action] = compute_q_value(q_value, cur_state, action, reward, new_state, predator)

            cur_state = new_state
            steps += 1
        episode_runs.append(steps)
        if i % (NUM_EPISODES/10) == 0:
            print i


    # for key in q_value:
    #     if q_value[key] > 1:
    #         print key
    #         print q_value[key]
    plt.plot(episode_runs)
    plt.show()
    print len(q_value)
if __name__ == '__main__':
    run_q_learning(verbose=True)
    print "Done."
