"""
Code was written in Python3. In this file, I did ...
Input variables are:

Return value:

Sample of how to use:

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""
from DropdownOptionMenu import DropdownOptionMenu
from GenerateExcelTable import GenerateExcelTable
from Person import Person
from get_years_remain_NO_screening import get_years_remain
from read_people_from_file import read_people_from_file

try:
    # Python3
    import tkinter as tk
except ImportError:
    # Python2
    import Tkinter as tk


class Main(tk.Frame):
    def __init__(self, root):
        self.root = root
        HEIGHT = 700
        WIDTH = 1550
        self.root.title("Lung Cancer MicroSimulation Analytic Model")
        self.root.iconbitmap('./images/lung_cancer1_icon.ico')
        canvas = tk.Canvas(self.root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        try:
            bg_image = tk.PhotoImage(file='./images/bg3.png')
            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.place(anchor='nw')
        except tk.TclError:
            print("cant read the ./images/bg2.png")
        self.root.attributes('-alpha',
                             1)  # Set the transparent application (<1) so that we can see the desktop background
        self.root.geometry("+10+10")  # put the main window next to the upper left corner

        # layout the frames
        frame1 = tk.Frame(root, bg="#5fb7fa")
        frame1.place(relx=0.005, rely=0.01, relwidth=0.99, relheight=0.29)
        frame2 = tk.Frame(self.root, bg="#5fb7fa")
        frame2.place(relx=0.005, rely=0.31, relwidth=0.19, relheight=0.65)
        frame3 = tk.Frame(self.root, bg="#5fb7fa", borderwidth=3)
        frame3.place(relx=0.20, rely=0.31, relwidth=0.795, relheight=0.65)
        frame4_progress = tk.Frame(self.root, bg="#5fb7fa")
        frame4_progress.place(relx=0.005, rely=0.97, relwidth=0.99, relheight=0.02)

        # Progress bar widget
        s = tk.ttk.Style()
        s.theme_use('default')  # ["clam", "alt", "default", "classic", {"aqua", "step"}]
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        progress = tk.ttk.Progressbar(frame4_progress, style="red.Horizontal.TProgressbar", orient=tk.HORIZONTAL,
                                      length=100,
                                      mode='determinate')
        progress.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        # creating age label
        age_label = tk.Label(frame1, text="Age", bg="#5fb7fa").place(x=2, y=5)
        self.age_choices = ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64',
                            '65',
                            '66',
                            '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
                            '82',
                            '83',
                            '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98',
                            '99']
        self.age_menu = DropdownOptionMenu(frame1, 30, 2, self.age_choices, 40)

        # creating gender label
        gender_label = tk.Label(frame1, text="Gender", bg="#5fb7fa").place(x=90, y=5)
        self.gender_choices = ['Male  ', 'Female']
        self.gender_menu = DropdownOptionMenu(frame1, 135, 2, self.gender_choices)

        # creating years smoked label
        smk_years_label = tk.Label(frame1, text="Smoking year", bg="#5fb7fa").place(x=220, y=5)
        self.smk_years_choices = ['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13',
                                  '14',
                                  '15']
        self.smk_years_menu = DropdownOptionMenu(frame1, 300, 2, self.smk_years_choices, 1)

        # creating years quit label
        qt_years_label = tk.Label(frame1, text="Quit year", bg="#5fb7fa").place(x=355, y=5)
        self.qt_years_choices = ['NA', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13',
                                 '14',
                                 '15']
        self.qt_years_menu = DropdownOptionMenu(frame1, 410, 2, self.qt_years_choices)

        # creating cigarettes per day label
        cpd_label = tk.Label(frame1, text="Cigarettes/day", bg="#5fb7fa").place(x=475, y=5)
        self.cpd_choices = ['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14',
                            '15']
        self.cpd_menu = DropdownOptionMenu(frame1, 560, 2, self.cpd_choices, 5)

        # creating race label ((0=Non-hispanic white, 1=Non-hispanic Black/African American, 2=Hispanic,
        # 3=Non-Hispanic American Indian/Alaska Native, 4=Non-Hispanic Asian or Pacific Islander, 5=Non-Hispanic Unknown Race)
        race_label = tk.Label(frame1, text="Race", bg="#5fb7fa").place(x=615, y=5)
        self.race_choices = ['Non-hispanic white', 'Non-hispanic Black/African American', 'Hispanic',
                             'Non-Hispanic American Indian/Alaska Native', 'Non-Hispanic Asian or Pacific Islander',
                             'Non-Hispanic Unknown Race']
        self.race_menu = DropdownOptionMenu(frame1, 650, 2, self.race_choices)

        # creating lung disease (1=COPD or Emphysema, 0=No COPD or Emphysema) label
        emp_label = tk.Label(frame1, text="Lung disease", bg="#5fb7fa").place(x=880, y=5)
        self.emp_choices = ['COPD or Emphysema', 'No COPD or Emphysema']
        self.emp_menu = DropdownOptionMenu(frame1, 955, 2, self.emp_choices)

        # creating number of parents with lung cancer (0,1,2) label
        flt_label = tk.Label(frame1, text="Parents with LC", bg="#5fb7fa").place(x=1135, y=5)
        self.flt_choices = ['0', '1', '2']
        # option_menu(frame1, 1225, 2, flt_choices)
        self.flt_menu = DropdownOptionMenu(frame1, 1225, 2, self.flt_choices)

        # creating bmi label
        bmi_label = tk.Label(frame1, text="BMI", bg="#5fb7fa").place(x=1280, y=5)
        self.bmi_entry = tk.Entry(frame1, width=6)
        self.bmi_entry.insert(tk.END, '24.62')
        self.bmi_entry.place(x=1310, y=5)

        # creating label for highest education level (  1=<12 grade, 2=HS graduate, 3=post hs/no college,
        #                                               4=associate degree/some college, 5=bachelors degree, 6=graduate school)
        edu6_label = tk.Label(frame1, text="Education", bg="#5fb7fa").place(x=1360, y=5)
        self.edu6_choices = ['<12 grade', 'HS graduate', 'post hs/no college', 'associate degree/some college',
                             'bachelors degree', 'graduate school']
        self.edu6_menu = DropdownOptionMenu(frame1, 1420, 2, self.edu6_choices)

        # Creating a GO image button
        photo = tk.PhotoImage(file=r"./images/Go-button_100.png")
        self.go_button = tk.Button(frame2, text='Go !', image=photo, bg="#5fb7fa", borderwidth=0, command=self.go)
        self.go_button.pack()

        # Run model for the person above Checkbox
        self.one_person_var = tk.IntVar()
        self.one_person_var.set(1)
        check_above = tk.Checkbutton(frame2, text="Run model for the person above", variable=self.one_person_var,
                                     bg="#5fb7fa").pack()

        # Read the list of people Checkbox
        self.list_people_var = tk.IntVar()
        tk.Checkbutton(frame2, text="Read the list of people data from", variable=self.list_people_var,
                       bg="#5fb7fa").pack()
        file_name_entry = tk.Entry(frame2, width=30)
        file_name_entry.insert(tk.END, 'lcrisk_tool.xlsx')
        file_name_entry.pack()

        # Button to generate excel table for every combination
        tk.Label(frame2, bg="#5fb7fa").pack()
        tk.Label(frame2, bg="#5fb7fa").pack()
        tk.Label(frame2, bg="#5fb7fa", fg="white",
                 text="____________________________________________________________").pack()
        tk.Label(frame2, bg="#5fb7fa").pack()
        tk.Label(frame2, bg="#5fb7fa").pack()
        tk.Button(frame2, text="Generate Excel Table For Every Combination", command=self.generate_excel_table).pack()

        output_label = tk.Label(frame3, bg="#5fb7fa", text='This is the output: ', anchor='nw', justify='left')
        output_label.pack()

        # Draw the output text and scrollbar
        S = tk.Scrollbar(frame3)
        self.output_text = tk.Text(frame3, height=4, width=200)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(side=tk.LEFT, fill=tk.Y)
        S.config(command=self.output_text.yview)
        self.output_text.config(yscrollcommand=S.set)

        # initiate_table_and_array_from_file()

        print("Starting GUI ...")
        self.root.mainloop()

    def generate_excel_table(self):
        GenerateExcelTable()

    def go(self):
        global LC_result

        if self.one_person_var.get():
            LC_result = self.run_model_for_1_person()

        if self.list_people_var.get():
            # read data from "lcrisk_tool.xlsx" file
            self.run_model_for_list_of_people("input/lcrisk_tool.xlsx")

    def run_model_for_1_person(self):
        if self.state_not_changing():
            return

        # disable GO button after it is already clicked
        self.go_button['state'] = 'disabled'

        self.output_text.insert(tk.END, "Start Analyzing Model... \n"
                                + "Age:" + self.age_menu.tk_var.get()
                                + " | Gender:" + self.gender_menu.tk_var.get()
                                + " | Smoking years:" + self.smk_years_menu.tk_var.get()
                                + " | Quit years:" + self.qt_years_menu.tk_var.get()
                                + " | Cigarettes/day:" + self.cpd_menu.tk_var.get()
                                + " | Race:" + self.race_menu.tk_var.get()
                                + " | Emp:" + self.emp_menu.tk_var.get()
                                + " | Parents with LC:" + self.flt_menu.tk_var.get()
                                + " | BMI:" + self.bmi_entry.get()
                                + " | Education:" + self.edu6_menu.tk_var.get()
                                + "\n ---------------------------- \n")

        p1 = Person(int(self.age_menu.tk_var.get())
                    , self.gender_choices.index(self.gender_menu.tk_var.get())
                    , self.smk_years_choices.index(self.smk_years_menu.tk_var.get())
                    , self.qt_years_choices.index(self.qt_years_menu.tk_var.get())
                    , self.cpd_choices.index(self.cpd_menu.tk_var.get())
                    , self.race_choices.index(self.race_menu.tk_var.get())
                    , self.emp_choices.index(self.emp_menu.tk_var.get())
                    , self.flt_choices.index(self.flt_menu.tk_var.get())
                    , float(self.bmi_entry.get())
                    , self.edu6_choices.index(self.edu6_menu.tk_var.get())
                    )
        global life_table, local_cancer, regional_cancer, distant_cancer, \
            basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F

        p1.initiate_LCRAT_1mon_risk(basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F)

        years_remain = get_years_remain(p1, life_table, local_cancer, regional_cancer, distant_cancer, progress, root,
                                        False)

        # years_remain_screening = get_years_remain_screening(p1, life_table, local_cancer, regional_cancer, distant_cancer,
        #                                                     progress, root, False)
        self.output_text.insert(tk.END, "Life years remain (NO Screening): " + str(years_remain[0])
                                # + "\nLife years remain (Screening): " + str(years_remain_screening)
                                + " \n ---------------------------- \n")
        self.output_text.see(tk.END)

        self.set_new_changing_state(p1)

        # enable GO button after done processing
        self.go_button['state'] = 'normal'
        return [p1, years_remain]

    def run_model_for_list_of_people(self, filename):
        self.output_text.insert(tk.END, "Start Analyzing Model for the list of people in file [" + filename + "] ...\n")

        people_list = read_people_from_file(filename)
        self.output_text.insert(tk.END, "There are [" + str(len(people_list)) + "] people :\n")

        total_years_remain = 0
        for i in range(len(people_list)):
            # people_list[i].initiate_LCRAT_1mon_risk(basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F)
            years_remain = get_years_remain(people_list[i], life_table, local_cancer, regional_cancer, distant_cancer,
                                            progress, root, False)
            self.output_text.insert(tk.END,
                                    "Person [" + str(people_list[i].ID) + "] Years remain: " + str(
                                        years_remain) + " \n")
            total_years_remain += years_remain

        self.output_text.insert(tk.END, "\nTotal life years remain: " + str(total_years_remain) + " \n")
        self.output_text.insert(tk.END,
                           "Average life years per person: " + str(total_years_remain / len(people_list)) + " \n")
        self.output_text.insert(tk.END, " ---------------------------- \n")

    def state_not_changing(self):
        global old_age_choice, old_gender_choices, old_smk_years_choices, old_qt_years_choices, old_cpd_choices, \
            old_race_choices, old_emp_choices, old_flt_choices, old_bmi_entry, old_edu6_choices

        if int(self.age_menu.tk_var.get()) != old_age_choice \
                or self.gender_choices.index(self.gender_menu.tk_var.get()) != old_gender_choices \
                or self.smk_years_choices.index(self.smk_years_menu.tk_var.get()) != old_smk_years_choices \
                or self.qt_years_choices.index(self.qt_years_menu.tk_var.get()) != old_qt_years_choices \
                or self.cpd_choices.index(self.cpd_menu.tk_var.get()) != old_cpd_choices \
                or self.race_choices.index(self.race_menu.tk_var.get()) != old_race_choices \
                or self.emp_choices.index(self.emp_menu.tk_var.get()) != old_emp_choices \
                or self.flt_choices.index(self.flt_menu.tk_var.get()) != old_flt_choices \
                or float(self.bmi_entry.get()) != old_bmi_entry \
                or self.edu6_choices.index(self.edu6_menu.tk_var.get()) != old_edu6_choices:
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
