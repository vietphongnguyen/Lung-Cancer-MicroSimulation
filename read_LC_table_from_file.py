# python3

"""
In this class, I did ... Input variables are:


example python code use:


Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""


import xlrd


def to_interval(s):
    return int(s.split()[0]) - 1


def to_sex(s):
    if s[0] == "M":
        return 0
    else:
        return 1


def to_race(s):
    s1 = s[0:18].lower()
    if s1 == "non-hispanic white": return 0
    if s1 == "non-hispanic black": return 1
    if s1 == "hispanic (all race": return 2
    if s1 == "non-hispanic ameri": return 3
    if s1 == "non-hispanic asian": return 4
    return 5


def to_age(s):
    return int((int(s[0:2]) - 40) / 10)


def to_survival(s):
    # print(s)


    # deal with missing data
    try:
        f = float(s)
    except ValueError:
        f = 50

    return f / 100   # number in %. So that 98% become 0.98


def read_LC_table_from_file(file_name):
    print("Reading LC table from file [" + file_name + "] ...", end="")
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
    input_worksheet = input_workbook.sheet_by_name("Survival rate-Local cancer")
    for i in range(1, input_worksheet.nrows):
        interval = to_interval(input_worksheet.cell_value(i, 1))
        sex = to_sex(input_worksheet.cell_value(i, 2))
        race = to_race(input_worksheet.cell_value(i, 3))
        age = to_age(input_worksheet.cell_value(i, 4))
        survival = to_survival(input_worksheet.cell_value(i, 5))
        # print(survival, interval, sex, race, age)
        table[interval - 1][sex][race][age] = survival

    print("done")
    return table


def test():
    # print(to_interval("120 month"))
    # print(to_sex("Female"))
    # print(to_race("Hispanic (All Races)"))
    # print(to_age("50-59 years"))
    # LC_table = read_LC_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    # print(LC_table[0][0])

    print(to_survival(" 98.5   "))

# test()
