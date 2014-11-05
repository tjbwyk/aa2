import timeit

from field import Field
from predator import Predator
from models.prey import Prey
from predatorpolicy import PredatorPolicy
from models.policies.preypolicy import PreyPolicy


def main():
    # start the first assignment
    # run 100 times and measure time
    runtimes = []
    iterations = []
    for n in xrange(100):
        start = timeit.default_timer()
        as011()
    return None


def as011(verbose=True):
    # create field and characters
    environment = Field(11, 11)
    fatcat = Predator((0, 0))
    fatcat.set_policy(PredatorPolicy(fatcat, environment))
    chip = Prey((5, 5))
    chip.set_policy(PreyPolicy(chip, environment))
    environment.add_player(fatcat)
    environment.add_player(chip)

    if verbose: print environment.print_field()
    i = 0
    while not environment.isEnded():
        fatcat.act()
        chip.act()
        # print environment
        i += 1

    print str(i) + " iterations"
    print environment.print_field()
    return i


if __name__ == '__main__':
    main()
