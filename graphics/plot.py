__author__ = 'fbuettner'
from matplotlib import pyplot as plt
import pkg_resources

def get_output_path():
    return pkg_resources.resource_filename("reports", "plot/")


def value_heatmap(values, colorbar=True, path=None):
    """
    Plots a value matrix as heatmap.
    :param values: the value matrix
    :param path: if given, save the plot to pdf at given path.
    :return: the figure object
    """
    plt.figure()
    plt.xlim(0, values.shape[1])
    plt.ylim(0, values.shape[0])
    heatmap = plt.pcolor(values)
    if colorbar:
        plt.colorbar()
    if path is not None:
        plt.savefig(path)
    return heatmap


def plot_steps(num_steps, pred_win, window_size=50, title=""):
    plt.figure()
    plt.plot([sum(num_steps[i-window_size:i])/window_size for i in xrange(window_size, len(num_steps), window_size)], color="blue")
    plt.plot([sum(pred_win[i-window_size:i])/window_size for i in xrange(window_size, len(pred_win), window_size)], color="red")
    plt.title(title)
    plt.savefig(get_output_path() + "num_steps.png")
