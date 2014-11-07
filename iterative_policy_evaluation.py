import numpy as np
from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.predatorpolicy import PredatorPolicy
from models.policies.preypolicy import PreyPolicy


def main():
    as012(verbose=False)


def calculate_value(state,field,policy,value,discount_factor):
    new_value = 0
    for state in policy.getNextStates():
        print state

    exit(1)
    return new_value

def as012(verbose=True):
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.set_policy(PredatorPolicy(predator, field))
    chip = Prey((5, 5))
    chip.set_policy(PreyPolicy(chip, field))
    field.add_player(predator)
    field.add_player(chip)

    change_epsilon = 0.001
    state_iterator = field.state_iterator()
    discount_factor = 0.5

    # Initialise value array and temp array:
    # TODO: (now for 2 players only, generalize later)
    value = np.zeros((field.width*field.height,field.width*field.height))


    while True:
        delta_value = 0
        for state in state_iterator:
            temp_value = value[state]

            value[state]= calculate_value(state,field,predator.policy,value,discount_factor)

            delta_value = max(delta_value,temp_value - value[state])

        if delta_value < change_epsilon:
            break



if __name__ == '__main__':
    main()
