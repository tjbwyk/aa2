import q_learning as ql
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools as it


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def moving_stdev(a, n=3):
    result = np.zeros(len(a) - n + 1)
    for i in range(0, len(a) - n + 1):
        try:
            result[i] = np.std(a[i:(i + n)])
        except:
            print i

    # result[(len(a)-n):len(a)] = 5
    return result


if __name__ == '__main__':
    learning_rate_values = [0.5]  # [0.01,0.1,0.2,0.5,0.9]
    discount_factor_values = [0.9, 0.7, 0.5, 0.1]  # ,0.7]#,0.7,0.9]
    epsilon_values = [0.05]
    value_init_values = [15]
    num_episodes = [10000]
    average_window = 200
    arg_list = (learning_rate_values, discount_factor_values, epsilon_values, value_init_values, num_episodes)
    mpl.rcParams['lines.linewidth'] = 0.5
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm']
    color_iter = enumerate(colors)
    for args in it.product(*arg_list):
        print args
        episode_runs = ql.run_q_learning(learning_rate=args[0], discount_factor=args[1], epsilon=args[2],
                                         value_init=args[3], num_episodes=args[4], verbose=True)
        avg = moving_average(episode_runs, average_window)
        stdev = moving_stdev(episode_runs, average_window)

        line = plt.plot(avg, alpha=0.5, label="lr=%s, df=%s. eps=%s, valueinit=%s" % args[0:4])
        plt.fill_between(range(0, len(stdev)), avg + 0.1 * stdev, avg - 0.1 * stdev, alpha=0.1,
                         facecolor=color_iter.next()[1])
    str_arg_list = tuple(str(a) for a in arg_list)
    plt.ylabel("steps per episode")
    plt.xlabel("episode #")
    plt.legend(fontsize=9)
    plt.savefig("reports/qlearning_lr%s_df%s_eps%s_valueinit%s_num_eps%s.pdf" % str_arg_list, bbox_inches='tight',
                interpolate=True)
    plt.savefig("reports/qlearning_lr%s_df%s_eps%s_valueinit%s_num_eps%s.png" % str_arg_list, bbox_inches='tight',
                interpolate=True)
    print "Done."