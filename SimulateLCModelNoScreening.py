import tkinter as tk


def str_sum(local_LC):
    sum = 0
    for i in local_LC:
        sum += i[0]
    return str(sum)

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
        self.window.title("Lung Cancer Risk Simulation Model - Years Remain Count (NO Screening)")
        self.window.iconbitmap('./images/lung_cancer1_icon.ico')
        # self.window.geometry("WIDTHxHEIGHT+0+0")
        canvas = tk.Canvas(self.window, height=HEIGHT, width=WIDTH)
        canvas.pack()
        try:
            path = './images/Lung cancer_2019-7-30_No Scanning1600x900 copy.png'
            bg_image = tk.PhotoImage(file=path)
            bg_label = tk.Label(self.window, image=bg_image)
            bg_label.place(anchor='nw')

        except tk.TclError:
            print("cant read the ./images/Lung cancer_2019-7-30_No Scanning1600x900 copy.png")
        self.window.geometry("+0+0")  # put the main window next to the upper left corner

        close_button = tk.Button(self.window, text="Click Here to Close This Window", command=self.quit)
        close_button.place(x=1250, y=600)

        # Display the disease free number
        tk.Label(self.window, text=str(disease_free)[:5]).place(x=225, y=157)   # , bg="green"

        # Display the death other causes
        tk.Label(self.window, text=str(death_other_causes)[:5]).place(x=1010, y=440)

        # Display the Local LC
        tk.Label(self.window, text=total_local_LC[:5]).place(x=225, y=295)

        # Display the Regional LC
        tk.Label(self.window, text=total_regional_LC[:5]).place(x=225, y=397)

        # Display the Distant LC
        tk.Label(self.window, text=total_distant_LC[:5]).place(x=225, y=495)

        # Display the Death LC
        tk.Label(self.window, text=total_distant_LC[:5]).place(x=630, y=550)

        # Display current age and life remain
        try:
            path = './images/current age pointer copy.png'
            pointer_image = tk.PhotoImage(file=path)
            pointer_label = tk.Label(self.window, image=pointer_image)
            pointer_label2 = tk.Label(self.window, image=pointer_image)
        except tk.TclError:
            print("cant read the ./images/current age pointer copy.png")
        x1 = int(1088 + (age - 50) * 9.505)
        x2 = int(x1 + years_remain * 9.505)
        pointer_label.place(x=x1, y=383)
        pointer_label2.place(x=x2, y=383)
        tk.Label(self.window, text=str(age) + " + " + str(years_remain)[:6]).place(x=x1-8, y=412)

        # Draw the life remain bar
        canvas.create_rectangle(x1, 383, x2, 383 + 5, outline="red", fill="red")

        self.window.mainloop()

    def quit(self):
        self.window.destroy()


