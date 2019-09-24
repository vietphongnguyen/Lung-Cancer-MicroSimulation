# python3

"""
In this class, I did ... Input variables are:


Example python code use:


Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

import tkinter as tk

from get_years_remain_NO_screening import str_sum


class SimulateLCModelNoScreening:
    def __init__(self, window, LC_result):
        # LC_result = [person, years_remain]
        # years_remain = [year remain, disease_free, local_LC, regional_LC, distant_LC, death_other_causes]
        # local_LC = [number of local_LC, month infected]
        try:
            person = LC_result[0]
            age = person.age
            years_remain_result = LC_result[1]
            years_remain = years_remain_result[0]
            disease_free = years_remain_result[1]
            local_LC = years_remain_result[2]
            regional_LC = years_remain_result[3]
            distant_LC = years_remain_result[4]
            death_other_causes = years_remain_result[5]
            total_local_LC = str_sum(local_LC)
            total_regional_LC = str_sum(regional_LC)
            total_distant_LC = str_sum(distant_LC)
        except TypeError:
            age = 50
            years_remain = 50
            disease_free = 1
            death_other_causes = 0
            total_local_LC = "0"
            total_regional_LC = "0"
            total_distant_LC = "0"

        self.window = window
        HEIGHT = 800
        WIDTH = 1600
        number_of_digit_display = 8
        self.window.title("Lung Cancer Risk Simulation Model - Years Remain Count (NO Screening)")
        self.window.iconbitmap('./images/lung_cancer1_icon.ico')
        # self.window.geometry("WIDTHxHEIGHT+0+0")
        self.canvas = tk.Canvas(self.window, height=HEIGHT, width=WIDTH)
        self.window.minsize(WIDTH, HEIGHT)
        self.canvas.pack()
        try:
            path = './images/Lung cancer_2019-7-30_No Scanning1600x900 copy.png'
            bg_image = tk.PhotoImage(file=path)
            bg_label = tk.Label(self.window, image=bg_image)
            bg_label.place(anchor='nw')

        except tk.TclError:
            print("cant read the ./images/Lung cancer_2019-7-30_No Scanning1600x900 copy.png")
        self.window.geometry("+0+0")  # put the main window next to the upper left corner

        # add button to Close the Window
        self.close_button = tk.Button(self.window, text="Click Here to Close This Window", command=self.quit)
        self.close_button.place(x=1250, y=600)

        # Display the death other causes
        tk.Label(self.window, text=str("{:.20f}".format(death_other_causes))[:number_of_digit_display],
                 font=("Helvetica", 12)) \
            .place(x=1010, y=430)

        # Display the disease free number
        tk.Label(self.window, text=str("{:.20f}".format(disease_free))[:number_of_digit_display], fg="green",
                 font=("Helvetica", 12)) \
            .place(x=205, y=157)

        # Display the Local LC
        tk.Label(self.window, text=total_local_LC[:number_of_digit_display], fg="yellow", bg="black",
                 font=("Helvetica", 12)) \
            .place(x=205, y=295)

        # Display the Regional LC
        tk.Label(self.window, text=total_regional_LC[:number_of_digit_display], fg="orange", font=("Helvetica", 12)) \
            .place(x=205, y=397)

        # Display the Distant LC
        tk.Label(self.window, text=total_distant_LC[:number_of_digit_display], fg="brown", font=("Helvetica", 12)) \
            .place(x=205, y=495)

        # Display the Death LC
        tk.Label(self.window, text=total_distant_LC[:number_of_digit_display], font=("Helvetica", 12)) \
            .place(x=610, y=550)

        # Display current age and life remain
        try:
            path = './images/current age pointer copy.png'
            pointer_image = tk.PhotoImage(file=path)
            pointer_label = tk.Label(self.window, image=pointer_image, bd=0, highlightthickness=2)
            pointer_label2 = tk.Label(self.window, image=pointer_image, bd=0, highlightthickness=2)
        except tk.TclError:
            print("cant read the ./images/current age pointer copy.png")
        x1 = int(1088 + (age - 50) * 9.505)
        x2 = int(x1 + years_remain * 9.505)

        # Draw the life remain bar
        canvas = tk.Canvas(self.window, cursor='circle', height=5, width=x2 - x1, bg="red", bd=0, highlightthickness=0)
        # "arrow"  "circle" "clock" "cross" "dotbox" "exchange" "fleur" "heart" "man" "mouse" "pirate" "plus" "shuttle"
        # "sizing" "spider" "spraycan" "star" "target" "tcross" "trek" "watch"
        canvas.place(x=x1 + 10, y=385)

        # display the remaining year
        pointer_label.place(x=x1, y=385)
        # pointer_label2.place(x=x2, y=385)
        tk.Label(self.window, text=str(age) + " + " + str("{:.20f}".format(years_remain))[:number_of_digit_display],
                 fg="red", font=("Helvetica", 12)) \
            .place(x=x1 - 20, y=412)

        self.window.mainloop()

    def quit(self):
        self.window.destroy()
