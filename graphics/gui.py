__author__ = 'fbuettner'
import Tkinter as tk

class GameFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_field_grid()

    def create_widgets(self):
        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()

    def create_field_grid(self):
        self.xoffset = self.yoffset = 20
        self.rows = 11
        self.columns = 11
        self.cellwidth = 30
        self.cellheight = 30
        self.width = 2 * self.xoffset + self.rows * self.cellwidth
        self.height = 2 * self.yoffset + self.columns * self.cellheight
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
        #self.predator_icon = tk.PhotoImage("images/predator.png")
        #self.prey_icon = tk.PhotoImage("images/prey.png")
        pass

    def draw_state(self, state):
        pass

if __name__ == "__main__":
    gui = GameFrame()
    gui.master.title("AA1-app")
    gui.mainloop()