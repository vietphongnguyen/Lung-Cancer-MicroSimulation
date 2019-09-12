# python3

"""
In this class, I did ... Input variables are:


example python code use:


Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""


import xlrd

from read_LC_table_from_file import to_interval, to_sex, to_age, to_race, to_survival


def read_distant_cancer_table_from_file(file_name):
    print("Reading Distant Cancer table from file [" + file_name + "] ...",end="")
    # Summary interval from 1 month to 120 months
    INTERVAL = 120
    # Sex: 0=male 1=female
    SEX = 2
    # Race and origin recode (NHW, NHB, NHAIAN, NHAPI, Hispanic)
    #   0=Non-Hispanic White,
    #   1=Non-Hispanic Black,
    #   2=Hispanic (All Races),
    #   3=Non-Hispanic American Indian/Alaska Native,
    #   4=Non-Hispanic Asian or Pacific Islander
    #   5=Non-Hispanic Unknown Race
    RACE = 6
    # Age deciles (40-49 years, 50-59 years, 60-69 years, 70-79 years, 80+ years)
    AGE = 5

    table = [[[[[] for i in range(AGE)] for i in range(RACE)] for i in range(SEX)] for i in range(INTERVAL)]

    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("Survival rate-Distant cancer")
    for i in range(1, input_worksheet.nrows):
        interval = to_interval(input_worksheet.cell_value(i, 1))
        sex = to_sex(input_worksheet.cell_value(i, 2))
        race = to_race(input_worksheet.cell_value(i, 3))
        age = to_age(input_worksheet.cell_value(i, 4))
        survival = to_survival(input_worksheet.cell_value(i, 5))
        # print(interval, sex, race, age)
        table[interval - 1][sex][race][age] = survival

    print("done")
    return table
