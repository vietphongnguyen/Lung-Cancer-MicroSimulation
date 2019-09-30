import unittest

import ConstantTables
from Person import get_model_coef_from_file, get_basehaz_from_file, Person
from get_years_remain_NO_screening import str_sum
from read_LC_table_from_file import read_LC_table_from_file
from read_distant_cancer_table_from_file import read_distant_cancer_table_from_file
from read_life_table_from_file import read_life_table_from_file
from read_people_from_file import read_people_from_file
from read_regional_cancer_table_from_file import read_regional_cancer_table_from_file


class TestGetYearsRemainNOScreening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ConstantTables.ConstantTables()

    def test_get_years_remain(self):
        # Person(age, gender, smkyears, qtyears, cpd, race, emp, fam_lung_trend, bmi, edu6)
        # p1 = Person(72, 1, 42, 6, 24, 2, 0, 2, 27, 5, 50.4, 0.000983915, 4)
        # p2 = Person(80, 0, 0, 0, 0, 0, 0, 0, 24.62, 0)
        # p3 = Person(99, 0, 1, 0, 5, 0, 0, 0, 24.62, 0)

        # Person[4],    age: 50(Female), smk_years: 2, qt_years: 6, cpd: 7(Non - Hispanic Asian or Pacific Islander,
        #               No COPD or Emphysema) fam_lung_trend: 1, bmi: 29.8(associate degree / some ...)
        p4 = Person(50, 1, 2, 6, 7, 4, 0, 1, 29.8, 4)

        p4.initiate_LCRAT_1mon_risk()

        years_remain = p4.get_years_remain_no_screening(None, None, True)

        print("Remain : {}".format(years_remain[0]))
        print("Disease_free : {}".format(years_remain[1]))
        # print("local_LC : {}".format(years_remain[2]))
        print("         local_LC Sum : {}".format(str_sum(years_remain[2])))

        print("         regional_LC Sum : {}".format(str_sum(years_remain[3])))
        print("         distant_LC Sum : {}".format(str_sum(years_remain[4])))
        print("death_other_causes : {}".format(years_remain[5]))

    def _test_read_people_from_file(self):
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

        people_list = read_people_from_file("input/lcrisk_tool.xlsx")
        # print(people_list[0].age)

        total_years_remain = 0
        for i in range(len(people_list)):
            # people_list[i].initiate_LCRAT_1mon_risk(basehaz_G, basehaz_H, basehaz_J, model_coef_D, model_coef_F)
            years_remain = get_years_remain(people_list[i], life_table, local_cancer, regional_cancer, distant_cancer,
                                            None, None, True)
            print("Years remain: " + str(years_remain) + " \n")
            total_years_remain += years_remain

        print("\n ------------------------ \nTotal life years remain: " + str(total_years_remain) + " \n")
        print(
            "Average life years per person: " + str(total_years_remain / len(people_list)) + " \n ----------------- \n")


if __name__ == '__main__':
    unittest.main()
