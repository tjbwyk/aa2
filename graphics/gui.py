__author__ = 'fbuettner'
import Tkinter as tk


class GameFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.xoffset = self.yoffset = 20
        self.rows = 11
        self.columns = 11
        self.cellwidth = 50
        self.cellheight = 50
        self.width = (2 * self.xoffset) + (self.rows * self.cellwidth)
        self.height = (2 * self.yoffset) + (self.columns * self.cellheight)
        self.state = ((0, 0), (0, 0))
        self.grid()
        self.create_field_grid()
        self.create_icons()
        self.draw_state(state=((1, 1), (5, 5)), trace=False)
        self.draw_state(state=((1, 3), (7, 5)), trace=True)
        self.draw_state(state=((0, 3), (7, 0)), trace=True)


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
        self.predator_icon = tk.PhotoImage(file="images/predator.gif")
        self.prey_icon = tk.PhotoImage(file="images/prey.gif")
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
            self.canvas.create_line(start.get("x"), start.get("y"), end.get("x"), end.get("y"), fill="red")
            # prey trace
            start = self.get_field_center(prey_location_old[0], prey_location_old[1])
            end = self.get_field_center(prey_location_new[0], prey_location_new[1])
            self.canvas.create_line(start.get("x"), start.get("y"), end.get("x"), end.get("y"), fill="blue")
        predator_dx = predator_location_new[0] - predator_location_old[0]
        predator_dy = predator_location_new[1] - predator_location_old[1]
        prey_dx = prey_location_new[0] - prey_location_old[0]
        prey_dy = prey_location_new[1] - prey_location_old[1]
        self.canvas.move(self.c_predator, predator_dx * self.cellwidth, predator_dy * self.cellheight)
        self.canvas.move(self.c_prey, prey_dx * self.cellwidth, prey_dy * self.cellheight)
        self.state = state
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
    gui = GameFrame()
    gui.master.title("AA1-GUI")
    gui.mainloop()