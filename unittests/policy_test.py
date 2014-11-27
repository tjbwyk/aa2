import unittest
from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy



class testPolicy(unittest.TestCase):
    def testPredatorPolicy(self):
        field = Field(11, 11)
        predator = Predator((0, 0))
        predator.policy = RandomPredatorPolicy(predator, field)
        chip = Prey((5, 5))
        chip.policy = RandomPreyPolicy(chip, field)
        field.add_player(predator)
        field.add_player(chip)
        predator.policy.pick_next_action(state=((1,1),(5,5)), style="foo")

    # def testPredatorPolicy(self):
    # field = Field(3, 3)
    #     predator = Predator((1, 1))
    #     policy = PredatorPolicy()
    #
    #     field.add_player(predator)
    #     field.print_field()
    #
    # def testPreyPolicy1(self):
    #     field = Field(3, 3)
    #     predator = Predator((1, 1))
    #     policy = PredatorPolicy()
    #
    #     field.add_player(predator)
    #     field.print_field()

    # def testGetStates(self):
    #     field = Field(3, 3)
    #     predator = Predator((1, 0))
    #     predator.set_policy(PredatorPolicy(agent=predator, field=field))
    #     field.add_player(predator)
    #     prey = Prey((0, 0))
    #     prey.set_policy(RandomPreyPolicy(agent=prey, field=field))
    #     field.add_player(prey)
    #
    #     trans, states = predator.policy.get_next_states()
    #     proba = 0.0
    #     for prob, a1, a2 in trans:
    #         proba += prob
    #
    #     print proba
    #     print trans, states


if __name__ == '__main__':
    unittest.main()
