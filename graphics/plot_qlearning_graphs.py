import q_learning as ql
import sarsa
import on_policy_evaluation as onpol
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import itertools as it

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def moving_stdev(a, n=3):
    result = np.zeros(len(a) - n + 1)
    for i in range(0, len(a)-n + 1):
        try:
            result[i] = np.std(a[i:(i+n)])
        except:
            print i

    # result[(len(a)-n):len(a)] = 5
    return result


if __name__ == '__main__':
    plot = 'steps_per_episode' #steps_per_episode or percentage

    learning_rate_values = [0.1]#[0.05,0.1,0.5,.9]
    discount_factor_values = [0.9]#,0.1,0.5,0.7,0.9,1]#,0.7]#,0.7,0.9]
    epsilon_values = [0.1]#,0.1]
    value_init_values = [15]#,5,15]
    num_episodes = [10000]
    tau = [0.01]#,0.1,0.2,0.5]
    policy_style=["softmax"]
    average_window = 500
    learning_algo = ["on-policy"] #"sarsa","qlearning"
    arg_list = (learning_rate_values,discount_factor_values,epsilon_values,value_init_values,num_episodes,tau,policy_style,learning_algo)
    mpl.rcParams['lines.linewidth'] = 0.5
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm']
    color_iter = enumerate(colors)
    for args in it.product(*arg_list):
        print args
        if args[7] == "on-policy":
            episode_runs = onpol.run(num_episodes=args[4])
            label = "on-policy"
        else:
            if args[7] == "sarsa":
                learning = sarsa
            elif args[7] == "qlearning":
                learning = ql
            episode_runs, q_value, percentage_correct= learning.run(learning_rate=args[0], discount_factor=args[1], epsilon=args[2],value_init=args[3], num_episodes=args[4], tau=args[5], policy_style=args[6],  verbose=True)
            label ="%s: $\\alpha=$%s, $\\gamma=$%s. $\\epsilon=$%s, initial value=%s, $\\tau =$%s, $\\pi=$%s" % ((args[7],)+ args[0:4] + args[5:7])

        if plot == 'percentage':
            avg = moving_average(percentage_correct,average_window)
            stdev = moving_stdev(percentage_correct, average_window)
        elif plot == 'steps_per_episode':
            avg = moving_average(episode_runs,average_window)
            stdev = moving_stdev(episode_runs, average_window)
        plt.plot(avg,alpha=0.5,label=label)
        plt.fill_between(range(0,len(stdev)),avg+0.2*stdev,avg-0.2*stdev,alpha=0.1,facecolor=color_iter.next()[1],interpolate=True)

    arg_list = arg_list[0:7]
    str_arg_list = tuple(str(a) for a in arg_list)
    if plot == 'percentage':
        plt.ylabel("percentage correct")
        plt.xlabel("episode # (moving average and stdev(area plot) window of %d)" % (average_window))
        plt.legend(fontsize=9, loc=4)
    elif plot == 'steps_per_episode':
        plt.ylabel("steps per episode")
        plt.xlabel("episode # (moving average and stdev*0.2 window of %d)" % (average_window))
        plt.legend(fontsize=9)
    # x1,x2,y1,y2 = plt.axis()
    # print x1,x2,y1,y2
    # plt.axes((x1,x2,y1,y2))

    axes = plt.gca()
    if plot == 'steps_per_episode':
        axes.set_ylim([0,30])
    else:
        pass
        # axes.set_ylim([0.5,1])
    plt.grid(True)
    learning_algo = "-".join(learning_algo)
    # plt.savefig("../reports/"+learning_algo+"_lr%s_df%s_eps%s_valueinit%s_num_eps%s_tau%s_policy%s.pdf" % str_arg_list, bbox_inches='tight')
    plt.savefig("../reports/"+learning_algo+"_lr%s_df%s_eps%s_valueinit%s_num_eps%s_tau%s_policy%s.png" % str_arg_list, bbox_inches='tight',dpi=200)
    print "Done."