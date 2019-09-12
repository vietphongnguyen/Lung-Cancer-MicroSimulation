# python3

"""
In this class, I did ... Input variables are:


example python code use:


Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

import tkinter as tk


class FileToSave:
    # f = FileToSave(frame_left, "Save to file :", "Life Remain Table - Age 50 100.xlsx")
    #         f.pack()
    def __init__(self, parent_frame, label_text, default_file_name):
        label = tk.Label(parent_frame, text=label_text)
        label.grid()

        # grid_info will return dictionary with all grid elements:row, column, ipadx, ipday, sticky, rowspan, columnspan
        r = label.grid_info()['row']  # Row of the button
        c = label.grid_info()['column']

        file_name = tk.Entry(parent_frame, width=50)
        file_name.insert(tk.END, default_file_name)
        file_name.grid(row=r, column=c + 1)
        tk.Button(parent_frame, text="Browse ...").grid(row=r, column=c + 2)

        self.file_name = file_name.get()
