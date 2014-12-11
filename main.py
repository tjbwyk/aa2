from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.plearners.probabilistic_plearner import ProbabilisticPlearner
from models.plearners.q_plearner import QPlearner
from models.plearners.sarsa_plearner import SarsaPlearner
from models.plearners.minimax_q_plearner import MiniMaxQPlearner
from models.plearners.wolf_phc import Wolf_phc
from graphics.gui import GameFrame
from models.state import State
import matplotlib.pyplot as plt
import itertools
import time

def run(n_episodes=1000, gui=False):
    """
    runs a simulation with 3 predators, one prey and random policies for all agents
    :return:
    """

    #initialize the environment
    field = Field(5, 5)
    num_episodes = 10**3

    pred1loc = (0, 0)
    pred2loc = (5, 4)
    pred3loc = (0, 10)
    preyloc = (2, 2)

    #initialize the predators
    predator1 = Predator(id="Plato", location=pred1loc)
    predator2 = Predator(id="Pythagoras", location=pred2loc)
    # predator3 = Predator(pred3loc)

    #probabilistic
    # predator1.plearner = ProbabilisticPlearner(field=field, agent=predator1)
    # predator2.plearner = ProbabilisticPlearner(field=field, agent=predator2)
    # predator3.plearner = ProbabilisticPlearner(field=field, agent=predator3)

    #greedy Q
    #predator1.plearner = SarsaPlearner.create_greedy_plearner(field=field, agent=predator1, value_init=0,epsilon=0.01)
    # predator2.plearner = SarsaPlearner.create_greedy_plearner(field=field, agent=predator2, value_init=0,epsilon=0.01)
    # predator1.plearner = QPlearner.create_greedy_plearner(field=field, agent=predator1, value_init=0)
    # predator2.plearner = QPlearner.create_greedy_plearner(field=field, agent=predator2, value_init=0)
    # predator3.plearner = QPlearner.create_greedy_plearner(field=field, agent=predator3)
    
    # wolf
    predator1.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator1)
    predator2.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator2)
    # predator3.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator3)

    #softmax Q
    #predator1.plearner = QPlearner.create_softmax_plearner(field=field, agent=predator1)
    #predator2.plearner = QPlearner.create_softmax_plearner(field=field, agent=predator2)
    # predator3.plearner = QPlearner.create_softmax_plearner(field=field, agent=predator3)

    #minimax q
    predator1.plearner = MiniMaxQPlearner(field=field,agent=predator1,end_alpha=0.01,num_episodes=num_episodes)

    field.add_player(predator1)
    # field.add_player(predator2)
    # field.add_player(predator3)
    #initialize the prey
    chip = Prey(id="Kant", location=preyloc)

    chip.plearner = ProbabilisticPlearner(field=field, agent=chip)
    #chip.plearner =  Wolf_phc.create_greedy_plearner(field=field, agent=chip, epsilon=0.01)
    #chip.plearner = QPlearner.create_softmax_plearner(field=field, agent=chip)
    chip.plearner = MiniMaxQPlearner(field=field,agent=chip,end_alpha=0.01,num_episodes=num_episodes)

    field.add_player(chip)

    field.init_players()

    # set GUI
    if gui:
        GUI = GameFrame(field=field)

    num_steps = []

    for i in range(0, n_episodes):
        predator1.location = pred1loc
        predator2.location = pred2loc
        #predator3.location = pred3loc
        chip.location = preyloc
        field.update_state()
        field.steps = 0
        # print field.get_current_state()
        #run the simulation
        while not field.is_ended():
            field.run_step()
            if gui and i == n_episodes-1:
                GUI.update()
                time.sleep(0.2)

        #print State.state_from_field(field)
        num_steps.append(field.steps)
        print i, field.steps
        # breakpoint
        #if i > 900:
        #    pass
        #run the simulation
        while not field.is_ended():
            field.run_step()
            # if gui:
            #     GUI.update()
            #     time.sleep(0.02)

        #print State.state_from_field(field)
        num_steps.append(field.steps)
        if i % 1000 == 0:
            print i
        # print State.state_from_field(field), field.steps, field.state.prey_is_caught()
        print State.state_from_field(field), field.steps, field.state.prey_is_caught()
        # print [str(state) + ": " + str([predator1.plearner.policy.value[State([state]),action] for action in predator1.get_actions() ])for state in itertools.product([-1,0,1],repeat=2)]
        # for action in chip.get_actions():
        #     print '1', action, predator1.plearner.policy.get_value(State([(0,-1),(0,1)]),action)
        #     print '2', action, predator2.plearner.policy.get_value(State([(0,-1),(0,1)]),action)

    #plot_steps(num_steps)
    step = 50
    plot_list = [sum(num_steps[i-step:i])/step for i in xrange(step, len(num_steps), step)]
    # print plot_list
    plot_steps(plot_list, title="moving average over "+str(step)+" episodes")


def plot_steps(num_steps, title=""):
    plt.figure()
    plt.plot(num_steps)
    plt.title(title)
    plt.savefig("num_steps.png")

if __name__ == '__main__':
    run(n_episodes=10000, gui=True)
