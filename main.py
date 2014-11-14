import timeit
from random_policy import random_policy_wrapper
from iterative_policy_evaluation import run_iterative_policy_evaluation
from policy_iteration import run_policy_iteration
from value_iteration import run_value_iteration


def main():
    start = timeit.default_timer()
    # 1.1 random policy
    random_policy_wrapper(n_runs=100)
    print_timestamp(start)
    # 1.2 iterative policy evaluation
    run_iterative_policy_evaluation()
    print_timestamp(start)
    # 1.3 policy iteration
    run_policy_iteration()
    print_timestamp(start)
    # 1.4 value iteration
    run_value_iteration(plot_values=False)
    print_timestamp(start)


def print_timestamp(start):
    print str(round(timeit.default_timer() - start, 3)) + " seconds elapsed"

if __name__ == '__main__':
    main()
