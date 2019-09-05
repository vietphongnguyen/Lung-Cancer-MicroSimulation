import tkinter as tk


class DropdownOptionMenu:
    def __init__(self, mainframe, x_pos, y_pos, choices, default=0):
        self.mainframe = mainframe
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.choices = choices

        # Create a Tkinter variable
        self.tk_var = tk.StringVar()
        self.tk_var.set(self.choices[default])  # set the default option
        self.popup_menu = tk.OptionMenu(self.mainframe, self.tk_var, *self.choices)
        self.popup_menu.place(x=self.x_pos, y=self.y_pos)

        # link function to change dropdown
        self.tk_var.trace('w', self.change_dropdown)

    # on change dropdown value
    def change_dropdown(self, *args):
        # print(self.tk_var.get())
        pass