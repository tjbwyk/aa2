from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.plearners.probabilistic_plearner import ProbabilisticPlearner
from models.plearners.q_plearner import QPlearner
from models.plearners.wolf_phc import Wolf_phc
from graphics.gui import GameFrame
import time

def run(gui=False):
    """
    runs a simulation with 3 predators, one prey and random policies for all agents
    :return:
    """

    #initialize the environment
    field = Field(11, 11)

    pred1loc = (5, 6)
    pred2loc = (5, 4)
    pred3loc = (0, 10)
    preyloc = (5, 5)

    #initialize the predators
    predator1 = Predator(id="Plato", location=pred1loc)
    predator2 = Predator(id="Pythagoras", location=pred2loc)
    # predator3 = Predator(pred3loc)

    # predator1.plearner = ProbabilisticPlearner(field=field, agent=predator1)
    # predator2.plearner = ProbabilisticPlearner(field=field, agent=predator2)
    # predator3.plearner = ProbabilisticPlearner(field=field, agent=predator3)

    # predator1.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator1)
    # predator2.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator2)
    # predator3.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator3)

    predator1.plearner = QPlearner.create_greedy_plearner(field=field, agent=predator1)
    predator2.plearner = QPlearner.create_greedy_plearner(field=field, agent=predator2)
    # predator3.plearner = QPlearner.create_softmax_plearner(field=field, agent=predator3)


    field.add_player(predator1)
    field.add_player(predator2)
    # field.add_player(predator3)
    #initialize the prey
    chip = Prey(id="Kant", location=preyloc)

    chip.plearner = ProbabilisticPlearner(field=field, agent=chip)
    # chip.plearner = QPlearner.create_greedy_plearner(field=field, agent=chip,value_init=0,epsilon=0.2)
    #chip.plearner = QPlearner.create_softmax_plearner(field=field, agent=chip)

    field.add_player(chip)

    field.init_players()

    # set GUI
    if gui:
        GUI = GameFrame(field=field)

    from models.state import State

    for i in range(0, 10000):
        predator1.location = pred1loc
        predator2.location = pred2loc
        #predator3.location = pred3loc
        chip.location = preyloc
        field.update_state()
        field.steps = 0

        #run the simulation
        while not field.is_ended():
            field.run_step()
            if gui:
                GUI.update()
                time.sleep(0.02)

        #print State.state_from_field(field)

        print State.state_from_field(field), field.steps, field.state.prey_is_caught()
        for action in chip.get_actions():
            print '1', action, predator1.plearner.policy.get_value(State([(0,-1),(0,1)]),action)
            print '2', action, predator2.plearner.policy.get_value(State([(0,-1),(0,1)]),action)
if __name__ == '__main__':
    run()
