# importing tkinter module 
from tkinter import *
from tkinter.ttk import *

# creating tkinter window 
root = Tk()

# Progress bar widget
s = Style()
s.theme_use('default')     # ["clam", "alt", "default", "classic", {"aqua", "step"}]
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress = Progressbar(root, orient=HORIZONTAL,
                       length=100, mode='determinate', style="red.Horizontal.TProgressbar")


# Function responsible for the updation
# of the progress bar value 
def bar():
    import time
    progress['value'] = 20
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 50
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 60
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    root.update_idletasks()
    time.sleep(1)

    progress['style'] = "green.Horizontal.TProgressbar"
    progress['value'] = 100


progress.pack(pady=10)

# This button will initialize 
# the progress bar 
Button(root, text='Start', command=bar).pack(pady=10)

# infinite loop 
mainloop() 