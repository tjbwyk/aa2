from random_policy import random_policy_wrapper
from iterative_policy_evaluation import run_iterative_policy_evaluation
from policy_iteration import run_policy_iteration
from value_iteration import run_value_iteration


def main():
    # 1.1 random policy
    random_policy_wrapper(n_runs=100)
    # 1.2 iterative policy evaluation
    run_iterative_policy_evaluation()
    # 1.3 policy iteration
    run_policy_iteration()
    # 1.4 value iteration
    run_value_iteration(plot_values=False)


if __name__ == '__main__':
    main()
