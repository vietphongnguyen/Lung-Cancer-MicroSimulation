"""
Code was written in Python3. This class will generate the life years remaining for every combination and save to an
excel file.
Input variables are: file name

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar

import xlsxwriter
from numpy import random

import ConstantTables
from DropdownOptionMenu import DropdownOptionMenu
from FileToSave import FileToSave
from Person import Person


class GenerateExcelTable:
    # set the distribution of age
    # age_choices = ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65',
    #     '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
    #     '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97',
    #     '98', '99' ]

    # use age_min to normalize the age array index starting from 0. Ex: age = 50 has index 0 in [not_done] array
    age_min = 50

    age_distribution = [
        50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28,
        27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3,
        2, 1
    ]

    age_rand_sum = sum(age_distribution)
    for i in range(0, len(age_distribution)):
        age_distribution[i] /= age_rand_sum

    # set the distribution of gender
    # gender_choices = ['Male  ', 'Female']
    gender_distribution = [1, 1]
    gender_rand_sum = sum(gender_distribution)
    for i in range(0, len(gender_distribution)):
        gender_distribution[i] /= gender_rand_sum

    # set the distribution of smoking years
    # smk_years_choices = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
    smk_years_min = 1
    smk_years_distribution = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    smk_years_rand_sum = sum(smk_years_distribution)
    for i in range(0, len(smk_years_distribution)):
        smk_years_distribution[i] /= smk_years_rand_sum

    # set the distribution of quitting years
    # qt_years_choices = ['0', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14',
    #                     '15']
    qt_years_distribution = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    qt_years_rand_sum = sum(qt_years_distribution)
    for i in range(0, len(qt_years_distribution)):
        qt_years_distribution[i] /= qt_years_rand_sum

    # set the distribution of cigarette per day
    # cpd_choices = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15',
    #                '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'
    #                ]  # > 20 or else
    cpd_min = 1
    cpd_distribution = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    cpd_rand_sum = sum(cpd_distribution)
    for i in range(0, len(cpd_distribution)):
        cpd_distribution[i] /= cpd_rand_sum

    # set the distribution of race
    # race_choices = ['Non-hispanic white', 'Non-hispanic Black/African American', 'Hispanic',
    #                 'Non-Hispanic American Indian/Alaska Native', 'Non-Hispanic Asian or Pacific Islander',
    #                 'Non-Hispanic Unknown Race']
    race_distribution = [1, 1, 1, 1, 1, 1]
    race_rand_sum = sum(race_distribution)
    for i in range(0, len(race_distribution)):
        race_distribution[i] /= race_rand_sum

    # set the distribution of Emphysema
    # emp_choices = ['COPD or Emphysema', 'No COPD or Emphysema']
    emp_distribution = [1, 1]
    emp_rand_sum = sum(emp_distribution)
    for i in range(0, len(emp_distribution)):
        emp_distribution[i] /= emp_rand_sum

    # set the distribution of family lung trend
    # fam_lung_trend_choices = ['0', '1', '2']
    fam_lung_trend_distribution = [1, 1, 1]
    fam_lung_trend_rand_sum = sum(fam_lung_trend_distribution)
    for i in range(0, len(fam_lung_trend_distribution)):
        fam_lung_trend_distribution[i] /= fam_lung_trend_rand_sum

    # set the distribution of BMI
    # bmi_choices = [15, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8, ... , 40.6, 40.7, 40.8, 40.9, 41 ]

    bmi_distribution = [71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111,
                        113, 115, 117, 119, 121, 123, 25, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147,
                        149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183,
                        185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 210, 209, 208, 207,
                        206, 205, 204, 203, 202, 201, 200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 189,
                        188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171,
                        170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153,
                        152, 151, 150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135,
                        134, 133, 132, 131, 130, 129, 128, 127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117,
                        116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98,
                        97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75,
                        74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52,
                        51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29,
                        28, 27, 26, 25, 24, 23, 22, 21
                        ]
    bmi_rand_sum = sum(bmi_distribution)
    for i in range(0, len(bmi_distribution)):
        bmi_distribution[i] /= bmi_rand_sum

    # set the distribution of education
    # edu6_choices = ['<12 grade', 'HS graduate', 'post hs/no college', 'associate degree/some college',
    # 'bachelors degree', 'graduate school']

    # edu6_choices start from 1. Edu6_min will be used for adjustment from edu6_draw to edu6 value
    # edu6 = edu6_draw + edu6_min
    edu6_min = 1

    edu6_distribution = [1, 2, 3, 4, 5, 4]
    edu6_rand_sum = sum(edu6_distribution)
    for i in range(0, len(edu6_distribution)):
        edu6_distribution[i] /= edu6_rand_sum

    def initiate_values(self):
        pass

    def start_new_file(self, file):
        file.update_file_name()

        workbook = xlsxwriter.Workbook(file.file_name)
        worksheet = workbook.add_worksheet("Year Remain - LC")

        currency_format = workbook.add_format({'num_format': '$#,##0'})
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})
        caption_format = workbook.add_format({'bold': True})
        caption_format.set_font_size(16)

        caption = 'Year Remain Tables - Local Cancer'

        # Set the columns widths.
        worksheet.set_column('A:L', 15)
        worksheet.set_column('I:I', 21)

        # Merge and Write the caption.
        worksheet.merge_range('A1:L1', caption, caption_format)

        p1 = Person(
            90,  # age
            0,  # gender
            43,  # smkyears
            0,  # qtyears
            36,  # cpd
            0,  # race
            0,  # emp
            0,  # fam_lung_trend
            23,  # bmi
            3,  # edu6
            1,  # ID
        )
        progress = None
        root_ = None
        person_id = 0
        age_choices = [
            '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65',
            '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
            '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97',
            '98', '99']
        gender_choices = ['Male  ', 'Female']
        smk_years_choices = ['0 ', '15']
        qt_years_choices = ['0', '15']
        cpd_choices = ['11', '30']  # > 20 or else
        race_choices = ['Non-hispanic white', 'Non-hispanic Black/African American', 'Hispanic',
                        'Non-Hispanic American Indian/Alaska Native', 'Non-Hispanic Asian or Pacific Islander',
                        'Non-Hispanic Unknown Race']
        emp_choices = ['COPD or Emphysema', 'No COPD or Emphysema']
        fam_lung_trend_choices = ['0', '1', '2']
        bmi_choices = ['18.5', '40']
        edu6_choices = ['<12 grade', 'HS graduate', 'post hs/no college', 'associate degree/some college',
                        'bachelors degree', 'graduate school']

        max_row = len(edu6_choices) * len(bmi_choices) * len(fam_lung_trend_choices) * len(emp_choices) \
                  * len(race_choices) * len(cpd_choices) * len(qt_years_choices) * len(smk_years_choices) \
                  * len(gender_choices) * len(age_choices)
        # 6 * 22 * 3 * 2 * 6 * 16 * 16 * 16 * 2 * age = 2,433,024 * age
        # Compact option: 6 * 2 * 3 * 2 * 6 * 2 * 2 * 2 * 2 * age = 6912 * age

        # Add a table to the worksheet.
        table_area = "A3:L" + str(max_row + 4)
        worksheet.add_table(table_area, {'last_column': 1, 'columns': [{'header': 'ID'},
                                                                       {'header': 'Age'},
                                                                       {'header': 'Gender'},
                                                                       {'header': 'Smoking Years'},
                                                                       {'header': 'Quiting Years'},
                                                                       {'header': 'CPD'},
                                                                       {'header': 'Race'},
                                                                       {'header': 'EMP'},
                                                                       {'header': 'Family Lung Cancer Trend'},
                                                                       {'header': 'BMI'},
                                                                       {'header': 'Education'},
                                                                       {'header': 'Year Remain'},
                                                                       ]
                                         })
        worksheet.freeze_panes(3, 0)

        for age_text in age_choices:
            age = int(age_text)
            if age < 95:  # limit the age for faster testing only people from age of 95
                continue
            for gender_text in gender_choices:
                gender = gender_choices.index(gender_text)
                for smkyears_text in smk_years_choices:
                    smkyears = int(smkyears_text)
                    for qtyears_text in qt_years_choices:
                        qtyears = int(qtyears_text)
                        for cpd_text in cpd_choices:
                            cpd = int(cpd_text)
                            for race_text in race_choices:
                                race = race_choices.index(race_text)
                                # if race > 0:  # limit the race = 0 (Non-hispanic white) only for faster testing
                                #     continue
                                for emp_text in emp_choices:
                                    emp = emp_choices.index(emp_text)
                                    for fam_lung_trend_text in fam_lung_trend_choices:
                                        fam_lung_trend = int(fam_lung_trend_text)
                                        for bmi_text in bmi_choices:
                                            bmi = float(bmi_text)
                                            for edu6_text in edu6_choices:
                                                edu6 = edu6_choices.index(edu6_text) + 1
                                                # if edu6 != 2:  # limit the edu6 = 2 (HS graduate) for faster testing
                                                #     continue
                                                p1.age = age
                                                p1.gender = gender
                                                p1.smkyears = smkyears
                                                p1.qtyears = qtyears
                                                p1.cpd = cpd
                                                p1.race = race
                                                p1.emp = emp
                                                p1.fam_lung_trend = fam_lung_trend
                                                p1.bmi = bmi
                                                p1.edu6 = edu6
                                                person_id += 1
                                                p1.ID = person_id

                                                p1.initiate_LCRAT_1mon_risk()
                                                years_remain = p1.get_years_remain_no_screening(progress, root_, False)

                                                row = "A" + str(3 + person_id)
                                                worksheet.write_row(row, [p1.ID, p1.age, p1.gender, p1.smkyears,
                                                                          p1.qtyears, p1.cpd, p1.race, p1.emp,
                                                                          p1.fam_lung_trend, p1.bmi, p1.edu6,
                                                                          years_remain[0]]
                                                                    )

        try_again = messagebox.YES
        while try_again == messagebox.YES:
            try:
                workbook.close()
                try_again = messagebox.NO
            except Exception as e:
                try_again = messagebox.askyesno("FileCreateError !", str(e) + " \nDo you want to try again ?")

        messagebox.showinfo("Done", "Create File [" + file.file_name + "] Successful ! ")

    def __init__(self):
        self.initiate_values()
        self.root = tk.Tk()
        self.root.title("Generate Excel Table")
        HEIGHT = 500
        WIDTH = 1000
        tk.Canvas(self.root, width=WIDTH, height=HEIGHT).pack()

        # layout the frames
        frame_top = tk.Frame(self.root, bg="green")
        frame_top.place(relx=0, rely=0, relwidth=1, relheight=0.9)
        frame_progress = tk.Frame(self.root, bg="blue")
        frame_progress.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

        # the Current age progress bar
        tk.Label(frame_progress, text="Current person:").place(relx=0.0, rely=0.1)
        self.progress_current_age = Progressbar(frame_progress, length=100)
        self.progress_current_age.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)
        tk.Button(frame_progress, text="Cancel", command=lambda: self.cancel_progress()) \
            .place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.31)

        # the Overall progress bar
        self.label_overall = tk.Label(frame_progress, text="Overall :")
        self.label_overall.place(relx=0.0, rely=0.5)
        self.progress_total = Progressbar(frame_progress, length=100)
        self.progress_total.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.3)
        tk.Button(frame_progress, text="Cancel", command=lambda: self.cancel_progress()) \
            .place(relx=0.9, rely=0.5, relwidth=0.1, relheight=0.31)

        # Device the top frame into a left and a right frames
        frame_left = tk.Frame(frame_top, bg="white")
        frame_left.place(relx=0, rely=0, relwidth=0.8, relheight=1)
        frame_right = tk.Frame(frame_top, bg="green")
        frame_right.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

        file = FileToSave(frame_left, "Save to file :", 'Year remain tables - Local Cancer.xlsx')

        tk.Label(frame_right, bg="green").pack()
        tk.Button(frame_right, text="Start a New File", command=lambda: self.start_new_file(file)).pack()
        tk.Button(frame_right, text="Resume to the File", command=lambda: self.start_new_file(file)).pack()
        tk.Label(frame_right, bg="green").pack()
        tk.Button(frame_right, text="Start a New File with Random People",
                  command=lambda: self.new_random_file(file)).pack()

        # creating number of people dropdown option menu
        tk.Label(frame_right, text="Number of people: ", bg="green", fg="white").place(x=10, y=120)
        number_of_people_choices = ['1 ', '3 ', '5 ', '10', '50', '100', '200', '500', '1_000', '1_500', '2_000',
                                    '5_000', '10_000', 'All ']
        self.number_of_people_menu = DropdownOptionMenu(frame_right, 120, 120, number_of_people_choices)

        self.root.mainloop()

    def new_random_file(self, file):
        global cancel_age_progress
        cancel_age_progress = False

        file.update_file_name()
        workbook = xlsxwriter.Workbook(file.file_name)
        worksheet = workbook.add_worksheet("Year Remain - LC")
        caption_format = workbook.add_format({'bold': True})
        caption_format.set_font_size(16)

        caption = 'Year Remain Tables - Local Cancer (Randomly Generated The Most Common People)'

        # Set the columns widths.
        worksheet.set_column('A:L', 15)
        worksheet.set_column('I:I', 21)

        # Merge and Write the caption.
        worksheet.merge_range('A1:L1', caption, caption_format)

        max_row = len(GenerateExcelTable.edu6_distribution) * len(GenerateExcelTable.bmi_distribution) \
                  * len(GenerateExcelTable.fam_lung_trend_distribution) * len(GenerateExcelTable.emp_distribution) \
                  * len(GenerateExcelTable.race_distribution) * len(GenerateExcelTable.cpd_distribution) \
                  * len(GenerateExcelTable.qt_years_distribution) * len(GenerateExcelTable.smk_years_distribution) \
                  * len(GenerateExcelTable.gender_distribution) * len(GenerateExcelTable.age_distribution)
        # max row = 40,590,720,000  --> TOO BIG

        try:
            max_id = int(self.number_of_people_menu.tk_var.get())  # maximum number of people to create
        except ValueError:
            max_id = 1_000_000_000
        max_row = max_id + 1
        # print(max_id)

        # Add a table to the worksheet.
        table_area = "A3:L" + str(max_row + 4)
        worksheet.add_table(table_area, {'last_column': 1, 'columns': [{'header': 'ID'},
                                                                       {'header': 'Age'},
                                                                       {'header': 'Gender'},
                                                                       {'header': 'Smoking Years'},
                                                                       {'header': 'Quiting Years'},
                                                                       {'header': 'CPD'},
                                                                       {'header': 'Race'},
                                                                       {'header': 'EMP'},
                                                                       {'header': 'Family Lung Cancer Trend'},
                                                                       {'header': 'BMI'},
                                                                       {'header': 'Education'},
                                                                       {'header': 'Year Remain'},
                                                                       ]
                                         })
        worksheet.freeze_panes(3, 0)

        person_id = 0
        repeat = True

        print("Start generating {} people randomly. Please wait ...".format(max_id))

        while repeat and not cancel_age_progress:
            if person_id >= max_id:  # limit the total number of people
                break

            self.label_overall['text'] = 'Overall : {:,}/{:,}'.format(person_id + 1, max_id)

            age_draw = Person.age_choices.index(
                random.choice(Person.age_choices, 1, p=GenerateExcelTable.age_distribution))
            gender_draw = Person.gender_choices.index(
                random.choice(Person.gender_choices, 1, p=GenerateExcelTable.gender_distribution))
            smk_years_draw = Person.smk_years_choices.index(random.choice(Person.smk_years_choices, 1,
                                                                          p=GenerateExcelTable.smk_years_distribution))
            qt_years_draw = Person.qt_years_choices.index(random.choice(Person.qt_years_choices, 1,
                                                                        p=GenerateExcelTable.qt_years_distribution))
            cpd_draw = Person.cpd_choices.index(
                random.choice(Person.cpd_choices, 1, p=GenerateExcelTable.cpd_distribution))
            race_draw = Person.race_choices.index(
                random.choice(Person.race_choices, 1, p=GenerateExcelTable.race_distribution))
            emp_draw = Person.emp_choices.index(
                random.choice(Person.emp_choices, 1, p=GenerateExcelTable.emp_distribution))
            fam_lung_trend_draw = Person.fam_lung_trend_choices.index(
                random.choice(Person.fam_lung_trend_choices, 1, p=GenerateExcelTable.fam_lung_trend_distribution))

            # bmi_draw is the index of a bmi value. Ex: bmi_draw = 0 then bmi = 15
            # bmi = float(Person.edu6_choices[bmi_draw])
            bmi_draw = Person.bmi_choices.index(
                random.choice(Person.bmi_choices, 1, p=GenerateExcelTable.bmi_distribution))

            edu6_draw = Person.edu6_choices.index(
                random.choice(Person.edu6_choices, 1, p=GenerateExcelTable.edu6_distribution))

            person_id += 1

            p = Person(age_draw + GenerateExcelTable.age_min, gender_draw,
                       smk_years_draw + GenerateExcelTable.smk_years_min, qt_years_draw,
                       cpd_draw + GenerateExcelTable.cpd_min, race_draw, emp_draw, fam_lung_trend_draw,
                       float(Person.bmi_choices[bmi_draw]), edu6_draw + GenerateExcelTable.edu6_min, person_id)

            p.print_to_screen()
            p.initiate_LCRAT_1mon_risk()
            years_remain = p.get_years_remain_no_screening(self.progress_current_age, self.root, True)

            row = "A" + str(3 + person_id)
            worksheet.write_row(row, [p.ID, p.age, Person.gender_choices[p.gender], p.smkyears, p.qtyears, p.cpd,
                                      Person.race_choices[p.race], Person.emp_choices[p.emp],
                                      p.fam_lung_trend, p.bmi,
                                      Person.edu6_choices[p.edu6 - GenerateExcelTable.edu6_min],

                                      # str("{:.20f}".format(x))[:number_of_digit_display]
                                      str("{:.2f}".format(years_remain[0]))
                                      ])

        # keep asking to save the file again after failing to do it.
        try_again = messagebox.YES
        while try_again == messagebox.YES:
            try:
                workbook.close()
                try_again = messagebox.NO

                # show the information box when done.
                messagebox.showinfo("Done", "Create File [" + file.file_name + "] Successful ! ", parent=self.root)
            except Exception as e:
                try_again = messagebox.askyesno("FileCreateError !", str(e) + " \nDo you want to try again ?")

        cancel_age_progress = False

    def new_random_file_with_duplicate_checking(self, file):
        file.update_file_name()
        workbook = xlsxwriter.Workbook(file.file_name)
        worksheet = workbook.add_worksheet("Year Remain - LC")
        caption_format = workbook.add_format({'bold': True})
        caption_format.set_font_size(16)

        caption = 'Year Remain Tables - Local Cancer (Randomly Generated The Most Common People)'

        # Set the columns widths.
        worksheet.set_column('A:L', 15)
        worksheet.set_column('I:I', 21)

        # Merge and Write the caption.
        worksheet.merge_range('A1:L1', caption, caption_format)

        progress_ = None
        root_ = None

        max_row = len(GenerateExcelTable.edu6_distribution) * len(GenerateExcelTable.bmi_distribution) \
                  * len(GenerateExcelTable.fam_lung_trend_distribution) * len(GenerateExcelTable.emp_distribution) \
                  * len(GenerateExcelTable.race_distribution) * len(GenerateExcelTable.cpd_distribution) \
                  * len(GenerateExcelTable.qt_years_distribution) * len(GenerateExcelTable.smk_years_distribution) \
                  * len(GenerateExcelTable.gender_distribution) * len(GenerateExcelTable.age_distribution)
        # max row = 40,590,720,000  --> TOO BIG

        max_id = 10  # maximum number of people to create
        max_row = max_id + 1

        # Add a table to the worksheet.
        table_area = "A3:L" + str(max_row + 4)
        worksheet.add_table(table_area, {'last_column': 1, 'columns': [{'header': 'ID'},
                                                                       {'header': 'Age'},
                                                                       {'header': 'Gender'},
                                                                       {'header': 'Smoking Years'},
                                                                       {'header': 'Quiting Years'},
                                                                       {'header': 'CPD'},
                                                                       {'header': 'Race'},
                                                                       {'header': 'EMP'},
                                                                       {'header': 'Family Lung Cancer Trend'},
                                                                       {'header': 'BMI'},
                                                                       {'header': 'Education'},
                                                                       {'header': 'Year Remain'},
                                                                       ]
                                         })
        worksheet.freeze_panes(3, 0)

        # initiate the [not_done] array to True, which use for visited people when calculating the remaining years
        not_done = [[[[[[[[[[0] * len(GenerateExcelTable.edu6_distribution)]
                           * len(GenerateExcelTable.bmi_distribution)]
                          * len(GenerateExcelTable.fam_lung_trend_distribution)]
                         * len(GenerateExcelTable.emp_distribution)]
                        * len(GenerateExcelTable.race_distribution)]
                       * len(GenerateExcelTable.cpd_distribution)]
                      * len(GenerateExcelTable.qt_years_distribution)]
                     * len(GenerateExcelTable.smk_years_distribution)]
                    * len(GenerateExcelTable.gender_distribution)] \
                   * len(GenerateExcelTable.age_distribution)

        person_id = 0
        repeat = True
        years_remain = None
        p = None
        repeat_person = 0  # count when the random method generate the same person
        repeat_person_max = 3  # the maximum number of time trying to create a new person before stop

        while repeat:
            if person_id >= max_id:  # limit the total number of people
                break

            age_draw = Person.age_choices.index(
                random.choice(Person.age_choices, 1, p=GenerateExcelTable.age_distribution))
            gender_draw = Person.gender_choices.index(
                random.choice(Person.gender_choices, 1, p=GenerateExcelTable.gender_distribution))
            smk_years_draw = Person.smk_years_choices.index(random.choice(Person.smk_years_choices, 1,
                                                                          p=GenerateExcelTable.smk_years_distribution))
            qt_years_draw = Person.qt_years_choices.index(random.choice(Person.qt_years_choices, 1,
                                                                        p=GenerateExcelTable.qt_years_distribution))
            cpd_draw = Person.cpd_choices.index(
                random.choice(Person.cpd_choices, 1, p=GenerateExcelTable.cpd_distribution))
            race_draw = Person.race_choices.index(
                random.choice(Person.race_choices, 1, p=GenerateExcelTable.race_distribution))
            emp_draw = Person.emp_choices.index(
                random.choice(Person.emp_choices, 1, p=GenerateExcelTable.emp_distribution))
            fam_lung_trend_draw = Person.fam_lung_trend_choices.index(
                random.choice(Person.fam_lung_trend_choices, 1, p=GenerateExcelTable.fam_lung_trend_distribution))

            # bmi_draw is the index of a bmi value. Ex: bmi_draw = 0 then bmi = 15
            # bmi = float(Person.edu6_choices[bmi_draw])
            bmi_draw = Person.bmi_choices.index(
                random.choice(Person.bmi_choices, 1, p=GenerateExcelTable.bmi_distribution))

            edu6_draw = Person.edu6_choices.index(
                random.choice(Person.edu6_choices, 1, p=GenerateExcelTable.edu6_distribution))

            print(age_draw, gender_draw, smk_years_draw, qt_years_draw, cpd_draw, race_draw, emp_draw,
                  fam_lung_trend_draw,
                  bmi_draw,
                  edu6_draw, " = ", end="")
            print(not_done[age_draw][gender_draw][smk_years_draw][qt_years_draw][cpd_draw][race_draw][emp_draw][
                      fam_lung_trend_draw]
                  [bmi_draw]
                  [edu6_draw])

            if not_done[age_draw][gender_draw][smk_years_draw][qt_years_draw][cpd_draw][race_draw][emp_draw][
                fam_lung_trend_draw][bmi_draw][edu6_draw] == 0:

                person_id += 1

                p = Person(age_draw + GenerateExcelTable.age_min, gender_draw,
                           smk_years_draw + GenerateExcelTable.smk_years_min, qt_years_draw,
                           cpd_draw + GenerateExcelTable.cpd_min, race_draw, emp_draw, fam_lung_trend_draw,
                           float(Person.bmi_choices[bmi_draw]), edu6_draw + GenerateExcelTable.edu6_min, person_id)

                p.print_to_screen()
                p.initiate_LCRAT_1mon_risk()
                years_remain = p.get_years_remain_no_screening(progress_, root_, True)

                row = "A" + str(3 + person_id)
                worksheet.write_row(row, [p.ID, p.age, p.gender, p.smkyears, p.qtyears, p.cpd, p.race, p.emp,
                                          p.fam_lung_trend, p.bmi, p.edu6, years_remain[0]])
                not_done[age_draw][gender_draw][smk_years_draw][qt_years_draw][cpd_draw][race_draw][emp_draw][
                    fam_lung_trend_draw][bmi_draw][edu6_draw] = years_remain[0]

                repeat_person = 0
            else:
                repeat_person += 1
                if repeat_person >= repeat_person_max:
                    repeat = False  # exit the loop if the random method can not find a new person after 5 time
                    print("Exit the loop because the random method can not find a new person after {} times"
                          .format(repeat_person_max))

            print("repeat_person = {}".format(repeat_person))

        # keep asking to save the file again after failing to do it.
        try_again = messagebox.YES
        while try_again == messagebox.YES:
            try:
                workbook.close()
                try_again = messagebox.NO

                # show the information box when done.
                messagebox.showinfo("Done", "Create File [" + file.file_name + "] Successful ! ")
            except Exception as e:
                try_again = messagebox.askyesno("FileCreateError !", str(e) + " \nDo you want to try again ?")

    cancel_age_progress = False

    @staticmethod
    def cancel_progress():
        global cancel_age_progress
        cancel_age_progress = True


if __name__ == "__main__":
    ConstantTables.ConstantTables.init_value()
    GenerateExcelTable()
