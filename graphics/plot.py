__author__ = 'fbuettner'
import numpy as np
from matplotlib import pyplot as plt

def value_heatmap(values, colorbar=True, path=None):
    """
    Plots a value matrix as heatmap.
    :param values: the value matrix
    :param path: if given, save the plot to pdf at given path.
    :return:
    """
    plt.xlim(0, values.shape[1])
    plt.ylim(0, values.shape[0])
    heatmap = plt.pcolor(values)
    if colorbar:
        plt.colorbar()
    if path is not None:
        plt.savefig(path)