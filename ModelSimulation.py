"""
the main startup GUI for the Lung Cancer Micro-Simulation program

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""
from Main import Main
from NavigationBar import NavigationBar
from StatusBar import StatusBar
from ToolBar import ToolBar

try:
    # Python3
    import tkinter as tk
except ImportError:
    # Python2
    import Tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.statusbar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.navbar = NavigationBar(self)
        self.main = Main(self)

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
