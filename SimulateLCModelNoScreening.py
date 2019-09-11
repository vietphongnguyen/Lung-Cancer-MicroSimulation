import tkinter as tk





class SimulateLCModelNoScreening:
    def __init__(self, window):
        self.window = window
        HEIGHT = 800
        WIDTH = 1600
        self.window.title("Lung Cancer Risk Simulation Model - Years Remain Count (NO Screening)")
        self.window.iconbitmap('./images/lung_cancer1_icon.ico')
        canvas = tk.Canvas(self.window, height=HEIGHT, width=WIDTH)
        canvas.pack()
        try:
            path = './images/Lung cancer_2019-7-30_No Scanning1600x900 copy.png'
            bg_image = tk.PhotoImage(file=path)
            bg_label = tk.Label(window, image=bg_image)
            bg_label.place(anchor='nw')

        except tk.TclError:
            print("cant read the ./images/Lung cancer_2019-7-30_No Scanning1600x900 copy.png")
        self.window.geometry("+0+0")  # put the main window next to the upper left corner

        close_button = tk.Button(self.window, text="Click Here to Close This Window", command=self.quit)
        close_button.place(x=1250, y=600)

        self.window.mainloop()

    def quit(self):
        self.window.destroy()

    # window_LC_model_no_screening = SimulateLCModelNoScreening()
