import xlrd
from person import Person


def read_people_from_file(file_name):
    people_list = []
    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("calculator")
    # print(input_worksheet.nrows)

    for i in range(1, input_worksheet.nrows):
        ID = int(input_worksheet.cell_value(i, 0))
        # print(ID)
        age = int(input_worksheet.cell_value(i, 1))
        gender = int(input_worksheet.cell_value(i, 2))
        smkyears = int(input_worksheet.cell_value(i, 3))
        cpd = int(input_worksheet.cell_value(i, 5))
        race = int(input_worksheet.cell_value(i, 6))
        emp = int(input_worksheet.cell_value(i, 7))
        fam_lung_trend = int(input_worksheet.cell_value(i, 8))
        bmi = input_worksheet.cell_value(i, 9)
        edu6 = input_worksheet.cell_value(i, 10)
        qtyears = int(input_worksheet.cell_value(i, 11))
        pkyr_cat = input_worksheet.cell_value(i, 12)
        # print(pkyr_cat)
        LCRAT_1mon_risk = input_worksheet.cell_value(i, 19)

        p = Person(age, gender, smkyears, qtyears, cpd, race, emp, fam_lung_trend, bmi, edu6, pkyr_cat, LCRAT_1mon_risk, ID)
        # print(p.ID)
        people_list.append(p)

    # print(people_list[0].ID)
    return people_list


# read_people_from_file("input/lcrisk_tool.xlsx")
