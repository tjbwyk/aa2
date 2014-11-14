from random_policy import random_policy_wrapper
from iterative_policy_evaluation import as012
from value_iteration import as014


def main():
    random_policy_wrapper(n_runs=100)
    # iterative policy evaluation
    as012()
    # value iteration
    as014(plot_values=True)


if __name__ == '__main__':
    main()
