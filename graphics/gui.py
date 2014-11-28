__author__ = 'fbuettner'
import Tkinter as tk
import time
from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy
import pkg_resources


class GameFrame(tk.Frame):

    def __init__(self, master=None, field=None, window_title=None):
        tk.Frame.__init__(self, master)
        self.root = tk.Tk()
        self.master.title(window_title if window_title is not None else "AA1-GUI")
        self.field = field
        self.rows = self.field.height
        self.columns = self.field.width
        self.xoffset = self.yoffset = 20
        self.cellwidth = 50
        self.cellheight = 50
        self.width = (2 * self.xoffset) + (self.rows * self.cellwidth)
        self.height = (2 * self.yoffset) + (self.columns * self.cellheight)
        self.state = ((0, 0), (0, 0))
        self.grid()
        self.create_field_grid()
        self.create_icons()
        self.root.update()
        self.root.after(25)
        #self.draw_state(state=((1, 1), (5, 5)), trace=False)
        #self.draw_state(state=((1, 3), (7, 5)), trace=True)
        #self.draw_state(state=((0, 3), (7, 0)), trace=True)

    def update(self, trace=True):
        self.draw_state(state=self.field.get_current_state_complete(), trace=trace)


    def create_widgets(self):
        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()

    def create_field_grid(self):
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        for row in range(self.rows):
            for column in range(self.columns):
                x1 = self.xoffset + row * self.cellheight
                x2 = x1 + self.cellheight
                y1 = self.yoffset + column * self.cellwidth
                y2 = y1 + self.cellwidth
                self.canvas.create_rectangle(x1, y1, x2, y2)

    def create_icons(self):
        self.predator_icon = tk.PhotoImage(file=pkg_resources.resource_filename('gui', 'images/predator.gif'))
        self.prey_icon = tk.PhotoImage(file=pkg_resources.resource_filename('gui', 'images/prey.gif'))
        self.prey_dead_icon = tk.PhotoImage(file=pkg_resources.resource_filename('gui', 'images/prey_dead.gif'))
        self.c_predator = self.canvas.create_image(self.xoffset, self.yoffset, anchor="nw", image=self.predator_icon)
        self.c_prey = self.canvas.create_image(self.xoffset, self.yoffset, anchor="nw", image=self.prey_icon)
        return None

    def draw_state(self, state, trace=False):
        predator_location_old, prey_location_old = self.state
        predator_location_new, prey_location_new = state
        if trace:
            # predator trace
            start = self.get_field_center(predator_location_old[0], predator_location_old[1])
            end = self.get_field_center(predator_location_new[0], predator_location_new[1])
            # add +1 to separate from blue line
            self.canvas.create_line(start.get("x")+1, start.get("y")+1, end.get("x")+1, end.get("y")+1, fill="red")
            # prey trace
            start = self.get_field_center(prey_location_old[0], prey_location_old[1])
            end = self.get_field_center(prey_location_new[0], prey_location_new[1])
            # subtract -1 to separate from red line (1px in between)
            self.canvas.create_line(start.get("x")-1, start.get("y")-1, end.get("x")-1, end.get("y")-1, fill="blue")
        predator_dx = predator_location_new[0] - predator_location_old[0]
        predator_dy = predator_location_new[1] - predator_location_old[1]
        prey_dx = prey_location_new[0] - prey_location_old[0]
        prey_dy = prey_location_new[1] - prey_location_old[1]
        # if both players are in the same cell, bake red background color and redraw images so they are on top
        if predator_location_new == prey_location_new:
            x1 = self.xoffset + predator_location_new[0] * self.cellheight
            x2 = x1 + self.cellheight
            y1 = self.yoffset + predator_location_new[1] * self.cellwidth
            y2 = y1 + self.cellwidth
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F0AFBB")
            self.canvas.create_image(x1, y1, anchor="nw", image=self.prey_dead_icon)
        self.canvas.move(self.c_predator, predator_dx * self.cellwidth, predator_dy * self.cellheight)
        self.canvas.move(self.c_prey, prey_dx * self.cellwidth, prey_dy * self.cellheight)
        self.state = state
        self.root.update()
        return None

    def get_field_center(self, col, row):
        """
        calculates the x and y pixel coordinates of the field at given column and row in the grid.
        :param col:
        :param row:
        :return: dictionary with elements x and y
        """
        x = self.xoffset + col * self.cellwidth + 0.5 * self.cellwidth
        y = self.yoffset + row * self.cellheight + 0.5 * self.cellheight
        return {"x": x, "y": y}


if __name__ == "__main__":
    environment = Field(11, 11)
    fatcat = Predator((0, 0))
    fatcat.policy = RandomPredatorPolicy(fatcat, environment)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, environment)
    environment.add_player(fatcat)
    environment.add_player(chip)
    gui = GameFrame(field=environment)
    gui.draw_state(environment.get_current_state_complete())
    i = 0
    while not environment.is_ended():
        fatcat.act()
        chip.act()
        # print environment
        gui.update()
        i += 1
        time.sleep(0.1)
    gui.mainloop()