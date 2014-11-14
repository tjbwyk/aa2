__author__ = 'fbuettner'
import timeit
import time

import numpy as np

from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy


def random_policy_wrapper(n_runs=1):
    # start the first assignment
    # run 100 times and measure time
    runtimes = []
    iterations = []
    for n in xrange(n_runs):
        start = timeit.default_timer()
        i = run_random_policy(verbose=False)
        time = timeit.default_timer() - start
        runtimes.append(time)
        iterations.append(i)
    runtimes = np.asarray(runtimes)
    iterations = np.asarray(iterations)
    print "Mean runtime: " + str(np.mean(runtimes)) + " (standard deviation: " + str(np.std(runtimes)) + ")"
    print "Mean number of iterations: " + str(np.mean(iterations)) + " (standard deviation: " + str(
        np.std(iterations)) + ")"
    return runtimes, iterations


def run_random_policy(verbose=True):
    if verbose:
        print "=== RANDOM POLICY ==="
    # create field and characters
    environment = Field(11, 11)
    fatcat = Predator((0, 0))
    fatcat.policy = RandomPredatorPolicy(fatcat, environment)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, environment)
    environment.add_player(fatcat)
    environment.add_player(chip)

    if verbose:
        print environment.print_field()
        time.sleep(1)

    i = 0
    while not environment.is_ended():
        fatcat.act()
        chip.act()
        print environment
        i += 1

    if verbose:
        print str(i) + " iterations"
        print environment.print_field()
    return i


if __name__ == '__main__':
    random_policy_wrapper(n_runs=100)
