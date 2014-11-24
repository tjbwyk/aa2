import q_learning as ql
import matplotlib.pyplot as plt
import numpy as np
import itertools as it

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

if __name__ == '__main__':
    learning_rate_values = [0.01,0.1,0.2,0.5,0.9]
    discount_factor_values = [0.7]#,0.7]#,0.7,0.9]
    epsilon_values = [0.1]
    value_init_values = [15]
    num_episodes = [10000]
    arg_list = (learning_rate_values,discount_factor_values,epsilon_values,value_init_values,num_episodes)
    iter = it.product(*arg_list)

    for args in iter:
        print args
        episode_runs = ql.run_q_learning(learning_rate=args[0], discount_factor=args[1], epsilon=args[2],value_init=args[3], num_episodes=args[4], verbose=True)
        plt.plot(moving_average(episode_runs,20),alpha=0.5,label="lr=%s, df=%s. eps=%s, valueinit=%s" % args[0:4])

    str_arg_list = tuple(str(a) for a in arg_list)
    plt.legend(fontsize=9)
    plt.savefig("reports/qlearning_lr%s_df%s_eps%s_valueinit%s_num_eps%s.pdf" % str_arg_list)
    print "Done."