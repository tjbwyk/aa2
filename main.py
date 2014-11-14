from random_policy import random_policy_wrapper
from iterative_policy_evaluation import run_iterative_policy_evaluation
from policy_iteration import run_policy_iteration
from value_iteration import run_value_iteration


def main():
    random_policy_wrapper(n_runs=100)
    # iterative policy evaluation
    run_iterative_policy_evaluation()
    # policy iteration
    run_policy_iteration()
    # value iteration
    run_value_iteration(plot_values=True)


if __name__ == '__main__':
    main()
