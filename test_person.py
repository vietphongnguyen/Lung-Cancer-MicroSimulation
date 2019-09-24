"""
Code was written in Python3. This is the test case for the Person Class

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""


import unittest

import ConstantTables
from Person import Person, get_model_coef_from_file, get_basehaz_from_file


class TestPerson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ConstantTables.ConstantTables()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basehaz_G(self):
        pass

    def test_basehaz_H(self):
        pass

    def test_basehaz_J(self):
        pass

    def test_model_coef_D(self):
        pass

    def test_model_coef_F(self):
        pass

    def test_LCRAT_1mon_risk(self):
        p1 = Person(
            72,  # age
            1,  # gender
            42,  # smkyears
            6,  # qtyears
            24,  # cpd
            2,  # race
            0,  # emp
            2,  # fam_lung_trend
            27,  # bmi
            5,  # edu6
        )
        expect_result = 0.000983915
        delta = 0.000000001
        p1.initiate_LCRAT_1mon_risk()
        # print(p1.LCRAT_1mon_risk)
        self.assertLessEqual(abs(p1.LCRAT_1mon_risk - expect_result), delta)

        p2 = Person(
            66,  # age
            0,  # gender
            43,  # smkyears
            0,  # qtyears
            36,  # cpd
            0,  # race
            0,  # emp
            0,  # fam_lung_trend
            23,  # bmi
            3,  # edu6
        )
        expected_result_2 = 0.00113835
        delta = 0.00000001
        p2.initiate_LCRAT_1mon_risk()
        # print(p2.LCRAT_1mon_risk)
        self.assertLessEqual(abs(p2.LCRAT_1mon_risk - expected_result_2), delta)


if __name__ == '__main__':
    unittest.main()

