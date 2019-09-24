# python3

"""
In this file, I wrote the main startup GUI for the Lung Cancer Micro-Simulation program

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

from tkinter import messagebox
from tkinter.ttk import Progressbar, Style

import ConstantTables
from DropdownOptionMenu import DropdownOptionMenu
from GenerateExcelTable import GenerateExcelTable
from Person import Person
from SimulateLCModelNoScreening import SimulateLCModelNoScreening
from read_people_from_file import read_people_from_file

if __name__ != "__main__":
    exit()

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

old_age_choice = None
old_gender_choices = None
old_smk_years_choices = None
old_qt_years_choices = None
old_cpd_choices = None
old_race_choices = None
old_emp_choices = None
old_flt_choices = None
old_bmi_entry = None
old_edu6_choices = None


def reset_old_value():
    global old_age_choice, old_gender_choices, old_smk_years_choices, old_qt_years_choices, old_cpd_choices, \
        old_race_choices, old_emp_choices, old_flt_choices, old_bmi_entry, old_edu6_choices

    old_age_choice = None
    old_gender_choices = None
    old_smk_years_choices = None
    old_qt_years_choices = None
    old_cpd_choices = None
    old_race_choices = None
    old_emp_choices = None
    old_flt_choices = None
    old_bmi_entry = None
    old_edu6_choices = None


def state_not_changing():
    if int(age_menu.tk_var.get()) != old_age_choice \
            or gender_choices.index(gender_menu.tk_var.get()) != old_gender_choices \
            or smk_years_choices.index(smk_years_menu.tk_var.get()) != old_smk_years_choices \
            or qt_years_choices.index(qt_years_menu.tk_var.get()) != old_qt_years_choices \
            or cpd_choices.index(cpd_menu.tk_var.get()) != old_cpd_choices \
            or race_choices.index(race_menu.tk_var.get()) != old_race_choices \
            or emp_choices.index(emp_menu.tk_var.get()) != old_emp_choices \
            or flt_choices.index(flt_menu.tk_var.get()) != old_flt_choices \
            or float(bmi_entry.get()) != old_bmi_entry \
            or edu6_choices.index(edu6_menu.tk_var.get()) != old_edu6_choices:
        return False
    return True


def set_new_changing_state(p):
    global old_age_choice, old_gender_choices, old_smk_years_choices, old_qt_years_choices, old_cpd_choices, \
        old_race_choices, old_emp_choices, old_flt_choices, old_bmi_entry, old_edu6_choices

    old_age_choice = p.age
    old_gender_choices = p.gender
    old_smk_years_choices = p.smkyears
    old_qt_years_choices = p.qtyears
    old_cpd_choices = p.cpd
    old_race_choices = p.race
    old_emp_choices = p.emp
    old_flt_choices = p.fam_lung_trend
    old_bmi_entry = p.bmi
    old_edu6_choices = p.edu6


def go():
    global LC_result

    if one_person_var.get():
        LC_result = run_model_for_1_person()

    if list_people_var.get():
        # read data from "lcrisk_tool.xlsx" file
        run_model_for_list_of_people("input/lcrisk_tool.xlsx")


def run_model_for_1_person():
    if state_not_changing():
        return

    # disable GO button after it is already clicked
    go_button['state'] = 'disabled'

    output_text.insert(tk.END, "Start Analyzing Model... \n"
                       + "Age:" + age_menu.tk_var.get()
                       + " | Gender:" + gender_menu.tk_var.get()
                       + " | Smoking years:" + smk_years_menu.tk_var.get()
                       + " | Quit years:" + qt_years_menu.tk_var.get()
                       + " | Cigarettes/day:" + cpd_menu.tk_var.get()
                       + " | Race:" + race_menu.tk_var.get()
                       + " | Emp:" + emp_menu.tk_var.get()
                       + " | Parents with LC:" + flt_menu.tk_var.get()
                       + " | BMI:" + bmi_entry.get()
                       + " | Education:" + edu6_menu.tk_var.get()
                       + "\n ---------------------------- \n")

    p1 = Person(int(age_menu.tk_var.get())
                , gender_choices.index(gender_menu.tk_var.get())
                , smk_years_choices.index(smk_years_menu.tk_var.get())
                , qt_years_choices.index(qt_years_menu.tk_var.get())
                , cpd_choices.index(cpd_menu.tk_var.get())
                , race_choices.index(race_menu.tk_var.get())
                , emp_choices.index(emp_menu.tk_var.get())
                , flt_choices.index(flt_menu.tk_var.get())
                , float(bmi_entry.get())
                , edu6_choices.index(edu6_menu.tk_var.get())
                )

    p1.initiate_LCRAT_1mon_risk()

    years_remain = p1.get_years_remain_no_screening(progress, root, False)

    # years_remain_screening = get_years_remain_screening(p1, life_table, local_cancer, regional_cancer, distant_cancer,
    #                                                     progress, root, False)
    output_text.insert(tk.END, "Life years remain (NO Screening): " + str(years_remain[0])
                       # + "\nLife years remain (Screening): " + str(years_remain_screening)
                       + " \n ---------------------------- \n")
    output_text.see(tk.END)

    set_new_changing_state(p1)

    # enable GO button after done processing
    go_button['state'] = 'normal'
    return [p1, years_remain]


def run_model_for_list_of_people(filename):
    output_text.insert(tk.END, "Start Analyzing Model for the list of people in file [" + filename + "] ...\n")

    people_list = read_people_from_file(filename)
    output_text.insert(tk.END, "There are [" + str(len(people_list)) + "] people :\n")

    total_years_remain = 0
    for i in range(len(people_list)):
        # people_list[i].initiate_LCRAT_1mon_risk(basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F)
        years_remain = people_list[i].get_years_remain_no_screening(progress, root, False)
        output_text.insert(tk.END, "Person [" + str(people_list[i].ID) + "] Years remain: " + str(years_remain) + " \n")
        total_years_remain += years_remain

    output_text.insert(tk.END, "\nTotal life years remain: " + str(total_years_remain) + " \n")
    output_text.insert(tk.END,
                       "Average life years per person: " + str(total_years_remain / len(people_list)) + " \n")
    output_text.insert(tk.END, " ---------------------------- \n")


def generate_excel_table():
    table = GenerateExcelTable()


root = tk.Tk()


###################################### Creating the main menu bar  ##################################################

def donothing():
    x = 0


def console_save_to_file():
    text = output_text.get("1.0", tk.END)
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
        console_clear()


def console_clear():
    output_text.delete("1.0", tk.END)
    reset_old_value()


LC_result = None


def show_LC_model_no_screening():
    window = tk.Toplevel(root)
    window_LC_model_no_screening = SimulateLCModelNoScreening(window, LC_result)


menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=donothing)
file_menu.add_command(label="Open", command=donothing)
file_menu.add_command(label="Save", command=donothing)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

console_menu = tk.Menu(menu_bar, tearoff=0)
console_menu.add_command(label="Clear", command=console_clear)
console_menu.add_command(label="Save to file", command=console_save_to_file)
console_menu.add_separator()
console_menu.add_command(label="Option", command=donothing)
menu_bar.add_cascade(label="Console", menu=console_menu)

option_menu = tk.Menu(menu_bar, tearoff=0)
option_menu.add_command(label="Config default values", command=donothing)
option_menu.add_command(label="Appearance", command=donothing)
menu_bar.add_cascade(label="Option", menu=option_menu)

disease_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Disease", menu=disease_menu)

simulation_menu = tk.Menu(menu_bar, tearoff=0)
simulation_menu.add_command(label="Lung Cancer Risk Simulation Model (NO Screening)",
                            command=show_LC_model_no_screening)
simulation_menu.add_command(label="Save to file", command=donothing)
simulation_menu.add_separator()
simulation_menu.add_command(label="Option", command=donothing)
menu_bar.add_cascade(label="Simulation", menu=simulation_menu)

window_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Window", menu=window_menu)

people_menu = tk.Menu(menu_bar, tearoff=0)
people_menu.add_command(label="Add 1 more person", command=donothing)
people_menu.add_command(label="Remove the last person", command=donothing)
menu_bar.add_cascade(label="People", menu=people_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help Index", command=donothing)
help_menu.add_command(label="About...", command=donothing)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

###################################### End creating the main menu bar  #############################################

HEIGHT = 700
WIDTH = 1550
root.title("Lung Cancer MicroSimulation Analytic Model")
root.iconbitmap('./images/lung_cancer1_icon.ico')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
try:
    bg_image = tk.PhotoImage(file='./images/bg3.png')
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(anchor='nw')
except tk.TclError:
    print("cant read the ./images/bg2.png")
root.attributes('-alpha', 1)  # Set the transparent application (<1) so that we can see the desktop background
root.geometry("+10+10")  # put the main window next to the upper left corner

# layout the frames
frame1 = tk.Frame(root, bg="#5fb7fa")
frame1.place(relx=0.005, rely=0.01, relwidth=0.99, relheight=0.29)
frame2 = tk.Frame(root, bg="#5fb7fa")
frame2.place(relx=0.005, rely=0.31, relwidth=0.19, relheight=0.65)
frame3 = tk.Frame(root, bg="#5fb7fa", borderwidth=3)
frame3.place(relx=0.20, rely=0.31, relwidth=0.795, relheight=0.65)
frame4_progress = tk.Frame(root, bg="#5fb7fa")
frame4_progress.place(relx=0.005, rely=0.97, relwidth=0.99, relheight=0.02)

# Progress bar widget
s = Style()
s.theme_use('default')  # ["clam", "alt", "default", "classic", {"aqua", "step"}]
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
progress = Progressbar(frame4_progress, style="red.Horizontal.TProgressbar", orient=tk.HORIZONTAL, length=100,
                       mode='determinate')
progress.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

# creating age label
age_label = tk.Label(frame1, text="Age", bg="#5fb7fa").place(x=2, y=5)
age_choices = ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66',
               '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83',
               '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']
age_menu = DropdownOptionMenu(frame1, 30, 2, age_choices, 40)

# creating gender label
gender_label = tk.Label(frame1, text="Gender", bg="#5fb7fa").place(x=90, y=5)
gender_choices = ['Male  ', 'Female']
gender_menu = DropdownOptionMenu(frame1, 135, 2, gender_choices)

# creating years smoked label
smk_years_label = tk.Label(frame1, text="Smoking year", bg="#5fb7fa").place(x=220, y=5)
smk_years_choices = ['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
smk_years_menu = DropdownOptionMenu(frame1, 300, 2, smk_years_choices, 1)

# creating years quit label
qt_years_label = tk.Label(frame1, text="Quit year", bg="#5fb7fa").place(x=355, y=5)
qt_years_choices = ['NA', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
qt_years_menu = DropdownOptionMenu(frame1, 410, 2, qt_years_choices)

# creating cigarettes per day label
cpd_label = tk.Label(frame1, text="Cigarettes/day", bg="#5fb7fa").place(x=475, y=5)
cpd_choices = ['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15',
               '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
cpd_menu = DropdownOptionMenu(frame1, 560, 2, cpd_choices, 5)

# creating race label ((0=Non-hispanic white, 1=Non-hispanic Black/African American, 2=Hispanic,
# 3=Non-Hispanic American Indian/Alaska Native, 4=Non-Hispanic Asian or Pacific Islander, 5=Non-Hispanic Unknown Race)
race_label = tk.Label(frame1, text="Race", bg="#5fb7fa").place(x=615, y=5)
race_choices = ['Non-hispanic white', 'Non-hispanic Black/African American', 'Hispanic',
                'Non-Hispanic American Indian/Alaska Native', 'Non-Hispanic Asian or Pacific Islander',
                'Non-Hispanic Unknown Race']
race_menu = DropdownOptionMenu(frame1, 650, 2, race_choices)

# creating lung disease (1=COPD or Emphysema, 0=No COPD or Emphysema) label
emp_label = tk.Label(frame1, text="Lung disease", bg="#5fb7fa").place(x=880, y=5)
emp_choices = ['COPD or Emphysema', 'No COPD or Emphysema']
emp_menu = DropdownOptionMenu(frame1, 955, 2, emp_choices)

# creating number of parents with lung cancer (0,1,2) label
flt_label = tk.Label(frame1, text="Parents with LC", bg="#5fb7fa").place(x=1135, y=5)
flt_choices = ['0', '1', '2']
# option_menu(frame1, 1225, 2, flt_choices)
flt_menu = DropdownOptionMenu(frame1, 1225, 2, flt_choices)

# creating bmi label
bmi_label = tk.Label(frame1, text="BMI", bg="#5fb7fa").place(x=1280, y=5)
bmi_entry = tk.Entry(frame1, width=6)
bmi_entry.insert(tk.END, '24.62')
bmi_entry.place(x=1310, y=5)

# creating label for highest education level (  1=<12 grade, 2=HS graduate, 3=post hs/no college,
#                                               4=associate degree/some college, 5=bachelors degree, 6=graduate school)
edu6_label = tk.Label(frame1, text="Education", bg="#5fb7fa").place(x=1360, y=5)
edu6_choices = ['<12 grade', 'HS graduate', 'post hs/no college', 'associate degree/some college',
                'bachelors degree', 'graduate school']
edu6_menu = DropdownOptionMenu(frame1, 1420, 2, edu6_choices)

# Creating a GO image button
go_photo = tk.PhotoImage(file=r"./images/Go-button_100.png")
go_button = tk.Button(frame2, text='Go !', image=go_photo, bg="#5fb7fa", borderwidth=0, command=go)
go_button.pack()

# Run model for the person above Checkbox
one_person_var = tk.IntVar()
one_person_var.set(1)
check_above = tk.Checkbutton(frame2, text="Run model for the person above", variable=one_person_var,
                             bg="#5fb7fa").pack()

# Read the list of people Checkbox
list_people_var = tk.IntVar()
tk.Checkbutton(frame2, text="Read the list of people data from", variable=list_people_var, bg="#5fb7fa").pack()
file_name_entry = tk.Entry(frame2, width=30)
file_name_entry.insert(tk.END, 'lcrisk_tool.xlsx')
file_name_entry.pack()

# Button to generate excel table for every combination
tk.Label(frame2, bg="#5fb7fa").pack()
tk.Label(frame2, bg="#5fb7fa").pack()
tk.Label(frame2, bg="#5fb7fa", fg="white", text="____________________________________________________________").pack()
tk.Label(frame2, bg="#5fb7fa").pack()
tk.Label(frame2, bg="#5fb7fa").pack()
tk.Button(frame2, text="Generate Excel Table For Every Combination", command=generate_excel_table).pack()

output_label = tk.Label(frame3, bg="#5fb7fa", text='This is the output: ', anchor='nw', justify='left')
output_label.pack()

# Draw the output text and scrollbar
S = tk.Scrollbar(frame3)
output_text = tk.Text(frame3, height=4, width=200)
S.pack(side=tk.RIGHT, fill=tk.Y)
output_text.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=output_text.yview)
output_text.config(yscrollcommand=S.set)

ConstantTables.ConstantTables.init_value()

print("Starting GUI ...")
root.mainloop()
