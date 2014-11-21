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
        self.width = 2 * self.xoffset + self.rows * self.cellwidth
        self.height = 2 * self.yoffset + self.columns * self.cellheight
        self.state = ((0, 0), (0, 0))
        self.grid()
        self.create_field_grid()
        self.create_icons()
        self.draw_state(state=((1, 1), (5, 5)))


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
                self.canvas.create_rectangle(x1, x2, y1, y2)

    def create_icons(self):
        self.predator_icon = tk.PhotoImage(file="images/predator.gif")
        self.prey_icon = tk.PhotoImage(file="images/prey.gif")
        self.c_predator = self.canvas.create_image(self.xoffset, self.yoffset, anchor="nw", image=self.predator_icon)
        self.c_prey = self.canvas.create_image(self.xoffset, self.yoffset, anchor="nw", image=self.prey_icon)
        return None

    def draw_state(self, state):
        predator_location_old, prey_location_old = self.state
        predator_location_new, prey_location_new = state
        self.canvas.move(self.c_predator, (predator_location_new[0] - predator_location_old[0]) * self.cellwidth,
                         (predator_location_new[1] - predator_location_old[1]) * self.cellheight)
        self.canvas.move(self.c_prey, (prey_location_new[0] - prey_location_old[0]) * self.cellwidth,
                         (prey_location_new[1] - prey_location_old[1]) * self.cellheight)
        self.state = state
        return None


if __name__ == "__main__":
    gui = GameFrame()
    gui.master.title("AA1-GUI")
    gui.mainloop()