from models.field import Field
from models.predator import Predator
from models.prey import Preys


def run():
    field = Field(11, 11)
    predator1 = Predator((10, 10))
    predator2 = Predator((10, 0))
    predator2 = Predator((0, 10))
    predator.policy = RandomPredatorPolicy(predator, field, value_init=value_init)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)
    raise NotImplementedError


if __name__ == '__main__':
    run()
