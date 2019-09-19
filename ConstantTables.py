"""
Code was written in Python3. These constant tables are read from input files [Copy of Lung cancer_7-19-2019.xlxs] and
[lcrisk_tool.xlsx]

Return the values of static tables:
life_table, local_cancer, regional_cancer, distant_cancer, basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F

Sample of how to use:

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""
from Person import get_model_coef_from_file, get_basehaz_from_file
from read_LC_table_from_file import read_LC_table_from_file
from read_distant_cancer_table_from_file import read_distant_cancer_table_from_file
from read_life_table_from_file import read_life_table_from_file
from read_regional_cancer_table_from_file import read_regional_cancer_table_from_file


class ConstantTables:
    life_table = None
    local_cancer = None
    regional_cancer = None
    distant_cancer = None
    basehaz_G = None
    basehaz_H = None
    basehaz_J = None
    model_coef_D = None
    model_coef_F = None

    @staticmethod
    def init_value():
        global life_table, local_cancer, regional_cancer, distant_cancer, \
            basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F

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

    def __init__(self):
        if ConstantTables.life_table is None:
            ConstantTables.init_value()
