from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.probabilistic_policy import *


def run():
    """
    runs a simulation with 3 predators, one prey and random policies for all agents
    :return:
    """

    #initialize the environment
    field = Field(11, 11)

    #initialize the predators
    predator1 = Predator((10, 10))
    predator2 = Predator((10, 0))
    predator3 = Predator((0, 10))
    predator1.policy = ProbabilisticPolicy(predator1, field)
    predator2.policy = ProbabilisticPolicy(predator2, field)
    predator3.policy = ProbabilisticPolicy(predator3, field)
    field.add_player(predator1)
    field.add_player(predator2)
    field.add_player(predator3)
    #initialize the prey
    chip = Prey((5, 5))
    chip.policy = ProbabilisticPolicy(chip, field)
    field.add_player(chip)

    #this has to be called manually in the beginning until todo has been fixed
    field.update_state()

    #run the simulation
    while not field.is_ended():
        field.run_step()

if __name__ == '__main__':
    run()
