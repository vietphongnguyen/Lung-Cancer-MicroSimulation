import xlrd


def read_life_table_from_file(file_name):
    print("Reading life table from file [" + file_name + "] ...", end="")
    table = []
    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("Life-table")
    for i in range(55, 106):
        row = []
        for j in range(10, 18):
            row.append(input_worksheet.cell_value(i, j))
        table.append(row)

    print("done")
    return table


# life_table = read_life_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
# print(life_table[0][0])
