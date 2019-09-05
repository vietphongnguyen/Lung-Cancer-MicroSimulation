from DropdownOptionMenu import DropdownOptionMenu
from person import Person, get_model_coef_from_file, get_basehaz_from_file
from read_LC_table_from_file import read_LC_table_from_file
from read_distant_cancer_table_from_file import read_distant_cancer_table_from_file
from read_life_table_from_file import read_life_table_from_file
from get_years_remain_NO_screening import get_years_remain
from read_people_from_file import read_people_from_file
from read_regional_cancer_table_from_file import read_regional_cancer_table_from_file

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk


def go():
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

    # print(int(age_menu.tk_var.get())
    #       , gender_choices.index(gender_menu.tk_var.get())
    #       , smk_years_choices.index(smk_years_menu.tk_var.get())
    #       , qt_years_choices.index(qt_years_menu.tk_var.get())
    #       , cpd_choices.index(cpd_menu.tk_var.get())
    #       , race_choices.index(race_menu.tk_var.get())
    #       , emp_choices.index(emp_menu.tk_var.get())
    #       , flt_choices.index(flt_menu.tk_var.get())
    #       , gender_choices.index(gender_menu.tk_var.get())
    #       , float(bmi_entry.get())
    #       , edu6_choices.index(edu6_menu.tk_var.get())
    #       )

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

    p1.initiate_LCRAT_1mon_risk(basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F)

    years_remain = get_years_remain(p1, life_table, local_cancer, regional_cancer, distant_cancer, False)

    output_text.insert(tk.END, "Life years remain: " + str(years_remain) + " \n ---------------------------- \n")
    output_text.see(tk.END)


def process_people_list():
    # read data from "lcrisk_tool.xlsx" file
    people_list = read_people_from_file("input/lcrisk_tool.xlsx")
    # print(people_list[0].ID)

    total_years_remain = 0
    for i in range(len(people_list)):
        years_remain = get_years_remain(people_list[i], life_table, local_cancer, regional_cancer, distant_cancer)
        total_years_remain += years_remain

    output_text.insert(tk.END, "Total life years remain: " + str(total_years_remain) + " \n")
    output_text.insert(tk.END,
                       "Average life years per person: " + str(total_years_remain / len(people_list)) + " \n")


root = tk.Tk()


def donothing():
    x = 0


# Creating the main menu bar
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=donothing)
file_menu.add_command(label="Open", command=donothing)
file_menu.add_command(label="Save", command=donothing)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

console_menu = tk.Menu(menu_bar, tearoff=0)
console_menu.add_command(label="Clear", command=donothing)
console_menu.add_command(label="Save to file", command=donothing)
console_menu.add_separator()
console_menu.add_command(label="Option", command=donothing)
menu_bar.add_cascade(label="Console", menu=console_menu)

option_menu = tk.Menu(menu_bar, tearoff=0)
option_menu.add_command(label="Config default values", command=donothing)
option_menu.add_command(label="Appearance", command=donothing)
menu_bar.add_cascade(label="Option", menu=option_menu)

disease_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Disease", menu=disease_menu)

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

HEIGHT = 600
WIDTH = 1550
root.title("Lung Cancer MicroSimulation Analytic Model")
root.iconbitmap('./images/lung_cancer1_icon.ico')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
try:
    bg_image = tk.PhotoImage(file='./images/bg2.png')
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(anchor='nw')
except tk.TclError:
    print("cant read the ./images/bg2.png")
root.attributes('-alpha', 1)  # Set the transparent application so that we can see the desktop background

# layout the frames
frame1 = tk.Frame(root, bg="#5fb7fa")
frame1.place(relx=0.005, rely=0.01, relwidth=0.99, relheight=0.49)
frame2 = tk.Frame(root, bg="#5fb7fa")
frame2.place(relx=0.005, rely=0.51, relwidth=0.19, relheight=0.48)
frame3 = tk.Frame(root, bg="#5fb7fa", borderwidth=3)
frame3.place(relx=0.20, rely=0.51, relwidth=0.795, relheight=0.48)

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
smk_years_menu = DropdownOptionMenu(frame1, 300, 2, smk_years_choices)

# creating years quit label
qt_years_label = tk.Label(frame1, text="Quit year", bg="#5fb7fa").place(x=355, y=5)
qt_years_choices = ['NA', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
qt_years_menu = DropdownOptionMenu(frame1, 410, 2, qt_years_choices)

# creating cigarettes per day label
cpd_label = tk.Label(frame1, text="Cigarettes/day", bg="#5fb7fa").place(x=475, y=5)
cpd_choices = ['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
cpd_menu = DropdownOptionMenu(frame1, 560, 2, cpd_choices)

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
photo = tk.PhotoImage(file=r"./images/Go-button_100.png")
tk.Button(frame2, text='Go !', image=photo, bg="#5fb7fa", borderwidth=0, command=go).pack()

# Checkbox
var1 = tk.IntVar()
var1.set(1)
check_above = tk.Checkbutton(frame2, text="Run model for the person above", variable=var1, bg="#5fb7fa").pack()
var2 = tk.IntVar()
tk.Checkbutton(frame2, text="Read the list of people data from", variable=var2, bg="#5fb7fa").pack()
file_name_entry = tk.Entry(frame2, width=30)
file_name_entry.insert(tk.END, 'lcrisk_tool.xlsx')
file_name_entry.pack()

output_label = tk.Label(frame3, bg="#5fb7fa", text='This is the output: ', anchor='nw', justify='left')
output_label.pack()

# Draw the output text and scrollbar
S = tk.Scrollbar(frame3)
output_text = tk.Text(frame3, height=4, width=200)
S.pack(side=tk.RIGHT, fill=tk.Y)
output_text.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=output_text.yview)
output_text.config(yscrollcommand=S.set)

# init reading data table
life_table = read_life_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
local_cancer = read_LC_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
regional_cancer = read_regional_cancer_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
distant_cancer = read_distant_cancer_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")

# initiate the basehaz and the model_coef array to calculate the LCRAT_1mon_risk
basehaz_G = get_basehaz_from_file("input/lcrisk_tool.xlsx", 6)
basehaz_H = get_basehaz_from_file("input/lcrisk_tool.xlsx", 7)
basehaz_J = get_basehaz_from_file("input/lcrisk_tool.xlsx", 9)
model_coef_D = get_model_coef_from_file("input/lcrisk_tool.xlsx", 3)
model_coef_F = get_model_coef_from_file("input/lcrisk_tool.xlsx", 5)

print("Starting GUI ...")
root.mainloop()
