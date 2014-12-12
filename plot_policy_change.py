__author__ = 'fbuettner'
from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.plearners.wolf_phc import Wolf_phc
from matplotlib import pyplot as plt
from graphics.plot import get_output_path
import timeit


def run(n_episodes=1000):
    # initialize the environment
    field = Field(3, 3)

    """
    initial state:
    | | | |
    |X|O|X|
    | | | |
    """
    pred1loc = (0, 1)
    pred2loc = (2, 1)
    preyloc = (1, 1)
    plot_state = ((1, 0), (-1, 0))
    action_right = (1, 0)
    action_left = (-1, 0)

    predator1 = Predator(id="Plato", location=pred1loc)
    predator2 = Predator(id="Pythagoras", location=pred2loc)
    predator1.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator1)
    predator2.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=predator2)
    field.add_player(predator1)
    field.add_player(predator2)
    chip = Prey(id="Kant", location=preyloc)
    chip.plearner = Wolf_phc.create_greedy_plearner(field=field, agent=chip, epsilon=0.01)
    field.add_player(chip)
    field.init_players()

    num_steps = []
    pred_win = []
    value_of_pred1_moving_right = []
    value_of_pred2_moving_left = []

    for i in range(0, n_episodes):
        predator1.location = pred1loc
        predator2.location = pred2loc
        chip.location = preyloc
        field.update_state()
        field.steps = 0
        #run the simulation
        while not field.is_ended():
            field.run_step()

        num_steps.append(field.steps)
        pred_win.append(field.state.prey_is_caught())
        value_of_pred1_moving_right.append(predator1.plearner.policy.value[plot_state, action_right])
        value_of_pred2_moving_left.append(predator2.plearner.policy.value[plot_state, action_left])

    # create plots
    plt.figure()
    p1 = plt.plot(value_of_pred1_moving_right, color="blue", label="prob. of pred1 moving right")
    p2 = plt.plot(value_of_pred2_moving_left, color="red", label="prob. of pred2 moving left")
    plt.legend(handles=[p1, p2])
    plt.title(str(n_episodes) + " episodes")
    plt.savefig(get_output_path() + "policychange_wolf_" + n_episodes)


if __name__ == "__main__":
    start = timeit.default_timer()
    run(n_episodes=1000)
    print "finished after", round(timeit.default_timer()-start, 3), "seconds."
