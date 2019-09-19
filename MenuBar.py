"""
Code was written in Python3. In this file, I did ...
Input variables are:

Return value:

Sample of how to use:

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""
from tkinter import messagebox

from SimulateLCModelNoScreening import SimulateLCModelNoScreening

try:
    # Python3
    import tkinter as tk
except ImportError:
    # Python2
    import Tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, parent):
        # tk.Menu.__init__()
        self.menu_bar = tk.Menu(parent)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.donothing)
        file_menu.add_command(label="Open", command=self.donothing)
        file_menu.add_command(label="Save", command=self.donothing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        console_menu = tk.Menu(self.menu_bar, tearoff=0)
        console_menu.add_command(label="Clear", command=self.console_clear)
        console_menu.add_command(label="Save to file", command=self.console_save_to_file)
        console_menu.add_separator()
        console_menu.add_command(label="Option", command=self.donothing)
        self.menu_bar.add_cascade(label="Console", menu=console_menu)

        option_menu = tk.Menu(self.menu_bar, tearoff=0)
        option_menu.add_command(label="Config default values", command=self.donothing)
        option_menu.add_command(label="Appearance", command=self.donothing)
        self.menu_bar.add_cascade(label="Option", menu=option_menu)

        disease_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Disease", menu=disease_menu)

        simulation_menu = tk.Menu(self.menu_bar, tearoff=0)
        simulation_menu.add_command(label="Lung Cancer Risk Simulation Model (NO Screening)",
                                    command=self.show_LC_model_no_screening)
        simulation_menu.add_command(label="Save to file", command=self.donothing)
        simulation_menu.add_separator()
        simulation_menu.add_command(label="Option", command=self.donothing)
        self.menu_bar.add_cascade(label="Simulation", menu=simulation_menu)

        window_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Window", menu=window_menu)

        people_menu = tk.Menu(self.menu_bar, tearoff=0)
        people_menu.add_command(label="Add 1 more person", command=self.donothing)
        people_menu.add_command(label="Remove the last person", command=self.donothing)
        self.menu_bar.add_cascade(label="People", menu=people_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index", command=self.donothing)
        help_menu.add_command(label="About...", command=self.donothing)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        parent.config(menu=self.menu_bar)

    def donothing(self):
        x = 0

    def console_save_to_file(self):
        text = self.output_text.get("1.0", tk.END)
        if not text.strip():
            return

        # save text in the console to a file
        import datetime
        now = datetime.datetime.now()
        f = open("output/console_" + now.strftime("%Y-%m-%d %Hh%Mm%Ss") + ".txt", "w+")
        f.write(text)
        f.close()
        ask = messagebox.askyesno("Saved Successfully !",
                                  "The text in the console was successfully saved to file [output/console_"
                                  + now.strftime("%Y-%m-%d %Hh%Mm%Ss")
                                  + ".txt] \nDo you want to reset to a empty console ?")
        if ask:
            self.console_clear()

    def console_clear(self):
        self.output_text.delete("1.0", tk.END)
        self.reset_old_value()

    def show_LC_model_no_screening(self):
        window = tk.Toplevel(self.parent)

        global LC_result
        window_LC_model_no_screening = SimulateLCModelNoScreening(window, LC_result)