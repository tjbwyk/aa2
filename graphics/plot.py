__author__ = 'fbuettner'
import numpy as np
from matplotlib import pyplot as plt
import operator


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


def action_values_relative(action_values, relative_state, colorbar=True, path=None):
    plot_height = abs(relative_state[0]) + 2
    plot_width = abs(relative_state[1]) + 2
    if relative_state[1] > 0:
        predator_position_row = 1
        prey_position_row = abs(relative_state[1]) + 1
    else:
        predator_position_row = abs(relative_state[1])
        prey_position_row = 0
    if relative_state[0] > 0:
        predator_position_col = 1
        prey_position_col = abs(relative_state[0]) + 1
    else:
        predator_position_col = abs(relative_state[0])
        prey_position_col = 0
    values = np.zeros((plot_height, plot_width))
    for state_action, value in action_values.iteritems():
        state, action = state_action
        if state == relative_state:
            action_row = predator_position_row + action[1]
            action_col = predator_position_col + action[0]
            values[action_row, action_col] = value
    plt.figure()
    plt.xlim(0, plot_width)
    plt.ylim(0, plot_height)
    heatmap = plt.pcolor(values, cmap="RdBu", vmin=np.min(values[np.nonzero(values)]), vmax=np.max(values))
    if colorbar:
        plt.colorbar()
    if path is not None:
        plt.savefig(path)
    return heatmap


def action_value_quiver_relative(action_values, field_dim=(11, 11), title=None, path=None):
    action_x = np.zeros(field_dim)
    action_y = np.zeros(field_dim)
    max_action_values = np.zeros(field_dim)
    prey_location = (np.floor(field_dim[0]/2), np.floor(field_dim[1]/2))
    for col in range(field_dim[0]):
        for row in range(field_dim[1]):
            relative_state = (prey_location[0] - col, prey_location[1] - row)
            state_actions = {}
            for (state, action), value in action_values.iteritems():
                if state == relative_state:
                    state_actions[action] = value
            max_action = max(state_actions.iteritems(), key=operator.itemgetter(1))[0]
            action_x[row, col] = max_action[0]
            action_y[row, col] = max_action[1]
            max_action_values[row, col] = state_actions[max_action]
    # avoid random arrow in the middle
    max_action_values[prey_location] = 0
    plt.figure()
    fig = plt.quiver(action_x*max_action_values, action_y*max_action_values)
    if title is not None:
        plt.title(title)
    if path is not None:
        plt.savefig(path)
    return fig