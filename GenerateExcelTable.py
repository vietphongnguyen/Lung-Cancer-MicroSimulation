"""
Code was written in Python3. This class will generate the life years remaining for every combination and save to an
excel file.
Input variables are: file name

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

import tkinter as tk
from tkinter import messagebox

import xlsxwriter
from tkinter.ttk import Progressbar

from xlsxwriter.exceptions import FileCreateError

import ConstantTables
from FileToSave import FileToSave
from Person import Person
from get_years_remain_NO_screening import get_years_remain


class GenerateExcelTable():
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
            if age < 85:  # limit the age for faster testing only people from age of 85 
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
                                if race > 0:  # limit the race = 0 (Non-hispanic white) only for faster testing
                                    continue
                                for emp_text in emp_choices:
                                    emp = emp_choices.index(emp_text)
                                    for fam_lung_trend_text in fam_lung_trend_choices:
                                        fam_lung_trend = int(fam_lung_trend_text)
                                        for bmi_text in bmi_choices:
                                            bmi = float(bmi_text)
                                            for edu6_text in edu6_choices:
                                                edu6 = edu6_choices.index(edu6_text) + 1
                                                if edu6 != 2:  # limit the edu6 = 2 (HS graduate) for faster testing
                                                    continue
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
                                                years_remain = get_years_remain(p1, progress, root_, False)

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

        file = FileToSave(frame_left, "Save to file :", 'Year remain tables - Local Cancer.xlsx')

        tk.Button(frame_right, text="Start a New File", command=lambda: self.start_new_file(file)).pack()
        tk.Button(frame_right, text="Resume to the File", command=lambda: self.start_new_file(file)).pack()

        self.root.mainloop()


def test_GenerateExcelTable():
    GenerateExcelTable()


if __name__ == "__main__":
    ConstantTables.ConstantTables()
    test_GenerateExcelTable()
