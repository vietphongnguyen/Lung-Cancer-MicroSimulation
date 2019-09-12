"""
Code was written in Python3. In this file, I did ...
Input variables are:

Return value:

Sample of how to use:

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

import tkinter as tk
from tkinter.ttk import Progressbar

from FileToSave import FileToSave


class GenerateExcelTable():
    def start_new_file(self, file):

        print(file.file_name)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Generate Excel Table")
        HEIGHT = 400
        WIDTH = 600
        tk.Canvas(self.root, width=WIDTH, height=HEIGHT).pack()

        # layout the frames
        frame_top = tk.Frame(self.root, bg="green")
        frame_top.place(relx=0, rely=0, relwidth=1, relheight=0.9)
        frame_progress = tk.Frame(self.root, bg="blue")
        frame_progress.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

        # the Current age progress bar
        tk.Label(frame_progress, text="Current :").place(relx=0.0, rely=0.1)
        progress_current_age = Progressbar(frame_progress, length=100)
        progress_current_age.place(relx=0.1, rely=0.1, relwidth=0.9, relheight=0.3)

        # the Overall progress bar
        tk.Label(frame_progress, text="Overall :").place(relx=0.0, rely=0.5)
        progress_total = Progressbar(frame_progress, length=100)
        progress_total.place(relx=0.1, rely=0.5, relwidth=0.9, relheight=0.3)

        # Device the top frame into a left and a right frames
        frame_left = tk.Frame(frame_top, bg="white")
        frame_left.place(relx=0, rely=0, relwidth=0.8, relheight=1)
        frame_right = tk.Frame(frame_top, bg="green")
        frame_right.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

        file = FileToSave(frame_left, "Save to file :", "Life Remain Table - Age 50 100.xlsx")

        tk.Button(frame_right, text="Start a New File", command=self.start_new_file(file)).pack()
        tk.Button(frame_right, text="Resume to the File", command=self.start_new_file(file)).pack()

        print(file.file_name)
        self.root.mainloop()


def test_GenerateExcelTable():
    GenerateExcelTable()


test_GenerateExcelTable()
