# python3

"""

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""

import math

import xlrd

import ConstantTables
from get_years_remain_NO_screening import get_years_remain_no_screening


def get_basehaz_from_file(file_name, column):
    print("Reading Baseline hazard/survival [column " + str(column) + "] from file [" + file_name + "] ...", end="")
    table = []

    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("basehaz")
    for i in range(4, input_worksheet.nrows):
        surv = float(input_worksheet.cell_value(i, column))
        table.append(surv)

    print("done")
    return table


def get_model_coef_from_file(file_name, column):
    print("Reading [model_coef] array [column " + str(column) + "] from file [" + file_name + "] ...", end="")
    table = [0, 1, 2, 3]

    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("model_coef")
    for i in range(4, 20):
        coef = float(0.0)
        try:
            coef = float(input_worksheet.cell_value(i - 1, column))
        except ValueError:
            pass
        table.append(coef)

    print("done")
    return table


class Person:
    age_choices = [
        '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65',
        '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81',
        '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97',
        '98', '99'
    ]
    gender_choices = ['Male', 'Female']
    smk_years_choices = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
    qt_years_choices = ['0', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15']
    cpd_choices = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'
                   ]  # > 20 or else
    race_choices = ['Non-hispanic white', 'Non-hispanic Black/African American', 'Hispanic',
                    'Non-Hispanic American Indian/Alaska Native', 'Non-Hispanic Asian or Pacific Islander',
                    'Non-Hispanic Unknown Race']
    emp_choices = ['COPD or Emphysema', 'No COPD or Emphysema']
    fam_lung_trend_choices = ['0', '1', '2']
    bmi_choices = [15, 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8, 15.9, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6,
                   16.7, 16.8, 16.9, 17, 17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8, 17.9, 18, 18.1, 18.2, 18.3,
                   18.4, 18.5, 18.6, 18.7, 18.8, 18.9, 19, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9, 20,
                   20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7, 20.8, 20.9, 21, 21.1, 21.2, 21.3, 21.4, 21.5, 21.6,
                   21.7, 21.8, 21.9, 22, 22.1, 22.2, 22.3, 22.4, 22.5, 22.6, 22.7, 22.8, 22.9, 23, 23.1, 23.2, 23.3,
                   23.4, 23.5, 23.6, 23.7, 23.8, 23.9, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 25,
                   25.1, 25.2, 25.3, 25.4, 25.5, 25.6, 25.7, 25.8, 25.9, 26, 26.1, 26.2, 26.3, 26.4, 26.5, 26.6,
                   26.7, 26.8, 26.9, 27, 27.1, 27.2, 27.3, 27.4, 27.5, 27.6, 27.7, 27.8, 27.9, 28, 28.1, 28.2, 28.3,
                   28.4, 28.5, 28.6, 28.7, 28.8, 28.9, 29, 29.1, 29.2, 29.3, 29.4, 29.5, 29.6, 29.7, 29.8, 29.9, 30,
                   30.1, 30.2, 30.3, 30.4, 30.5, 30.6, 30.7, 30.8, 30.9, 31, 31.1, 31.2, 31.3, 31.4, 31.5, 31.6,
                   31.7, 31.8, 31.9, 32, 32.1, 32.2, 32.3, 32.4, 32.5, 32.6, 32.7, 32.8, 32.9, 33, 33.1, 33.2, 33.3,
                   33.4, 33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9, 35,
                   35.1, 35.2, 35.3, 35.4, 35.5, 35.6, 35.7, 35.8, 35.9, 36, 36.1, 36.2, 36.3, 36.4, 36.5, 36.6,
                   36.7, 36.8, 36.9, 37, 37.1, 37.2, 37.3, 37.4, 37.5, 37.6, 37.7, 37.8, 37.9, 38, 38.1, 38.2, 38.3,
                   38.4, 38.5, 38.6, 38.7, 38.8, 38.9, 39, 39.1, 39.2, 39.3, 39.4, 39.5, 39.6, 39.7, 39.8, 39.9, 40,
                   40.1, 40.2, 40.3, 40.4, 40.5, 40.6, 40.7, 40.8, 40.9, 41
                   ]
    edu6_choices = ['<12 grade', 'HS graduate', 'post hs/no college', 'associate degree/some college',
                    'bachelors degree', 'graduate school']

    def __init__(self, age, gender, smkyears, qtyears, cpd, race, emp, fam_lung_trend, bmi, edu6, ID=0):
        self.ID = ID
        self.age = age  # current age (numeric)
        self.gender = gender  # gender value (1=Female, 0=Male)
        self.smkyears = smkyears  # years smoked (numeric)
        self.qtyears = qtyears  # years quit (numeric or NA)
        self.cpd = cpd  # cigarettes per day (numeric)
        self.race = race  # race value (0=Non-hispanic white,
        #                   1=Non-hispanic Black/African American,
        #                   2=Hispanic, (>=3)=Other Ethnicity)
        #                   3=Non-Hispanic American Indian/Alaska Native
        #                   4=Non-Hispanic Asian or Pacific Islander
        #                   5=Non-Hispanic Unknown Race
        self.emp = emp  # lung disease (1=COPD or Emphysema, 0=No COPD or Emphysema)
        self.fam_lung_trend = fam_lung_trend  # number of parents with lung cancer (0,1,2)
        self.bmi = bmi  # bmi value (numeric)
        self.edu6 = edu6    # highest education level ( 1=<12 grade, 2=HS graduate, 3=post hs/no college,
        #                                               4=associate degree/some college, 5=bachelors degree,
        #                                               6=graduate school)

    def initiate_LCRAT_1mon_risk(self):

        # LCRAT_RR = EXP(   calculator!C2*model_coef!$D$4
        #                   +(IF(calculator!G2=1,1,0))*model_coef!$D$5
        #                   +(IF(calculator!G2=2,1,0))*model_coef!$D$6
        #                   +(IF(calculator!G2=3,1,0))*model_coef!$D$7
        #                   +calculator!K2*model_coef!$D$8
        #                   +calculator!I2*model_coef!$D$9
        #                   +calculator!H2*model_coef!$D$10
        #                   +(IF(calculator!J2<=18.5,1,0))*model_coef!$D$11
        #                   +(IF(calculator!F2>20,1,0))*model_coef!$D$12
        #                   +(IF(calculator!M2>=30 & calculator!M2<40,1,0))*model_coef!$D$13
        #                   +(IF(calculator!M2>=40 & calculator!M2<50,1,0))*model_coef!$D$14
        #                   +(IF(calculator!M2>=50,1,0))*model_coef!$D$15
        #                   +LN(calculator!B2)*model_coef!$D$16
        #                   +LN(calculator!J2)*model_coef!$D$17
        #                   +LN(IF(calculator!E2="NA",0,calculator!E2)+1)*model_coef!$D$18
        #                   +calculator!D2*model_coef!$D$19
        #                )

        # calculator!C2 * model_coef!$D$4
        x = self.gender * ConstantTables.model_coef_D[4]

        # +(IF(calculator!G2=1,1,0))*model_coef!$D$5
        if self.race == 1:
            x += ConstantTables.model_coef_D[5]

        # +(IF(calculator!G2=2,1,0))*model_coef!$D$6
        if self.race == 2:
            x += ConstantTables.model_coef_D[6]

        # +(IF(calculator!G2=3,1,0))*model_coef!$D$7
        if self.race == 3:
            x += ConstantTables.model_coef_D[7]

        # +calculator!K2*model_coef!$D$8
        x += self.edu6 * ConstantTables.model_coef_D[8]

        #  +calculator!I2*model_coef!$D$9
        x += self.fam_lung_trend * ConstantTables.model_coef_D[9]

        # +calculator!H2*model_coef!$D$10
        x += self.emp * ConstantTables.model_coef_D[10]

        # +(IF(calculator!J2<=18.5,1,0))*model_coef!$D$11
        if self.bmi <= 18.5:
            x += ConstantTables.model_coef_D[11]

        # +(IF(calculator!F2>20,1,0))*model_coef!$D$12
        if self.cpd > 20:
            x += ConstantTables.model_coef_D[12]

        # +(IF(calculator!M2>=30 & calculator!M2<40,1,0))*model_coef!$D$13
        self.pkyr_cat = self.smkyears * self.cpd / 20  # pkyr_cat = D2 * F2 / 20
        if 30 <= self.pkyr_cat < 40:
            x += ConstantTables.model_coef_D[13]

        # +(IF(calculator!M2>=40 & calculator!M2<50,1,0))*model_coef!$D$14
        if 40 <= self.pkyr_cat < 50:
            x += ConstantTables.model_coef_D[14]

        # +(IF(calculator!M2>=50,1,0))*model_coef!$D$15
        if self.pkyr_cat >= 50:
            x += ConstantTables.model_coef_D[15]

        #  +LN(calculator!B2)*model_coef!$D$16
        x += math.log(self.age) * ConstantTables.model_coef_D[16]

        #  +LN(calculator!J2)*model_coef!$D$17
        x += math.log(self.bmi) * ConstantTables.model_coef_D[17]

        # +LN(IF(calculator!E2="NA",0,calculator!E2)+1)*model_coef!$D$18
        x += math.log(self.qtyears + 1) * ConstantTables.model_coef_D[18]

        # +calculator!D2*model_coef!$D$19
        x += self.smkyears * ConstantTables.model_coef_D[19]

        self.LCRAT_RR = math.exp(x)

        # cox_death_RR = EXP(   calculator!C2*model_coef!$F$4
        #                       + (IF(calculator!G2=1,1,0))*model_coef!$F$5
        #                       + (IF(calculator!G2=2,1,0))*model_coef!$F$6
        #                       + (IF(calculator!G2=3,1,0))*model_coef!$F$7
        #                       + calculator!K2*model_coef!$F$8
        #                       + calculator!H2*model_coef!$F$9
        #                       + (IF(calculator!J2<=18.5,1,0))*model_coef!$F$10
        #                       + (IF(calculator!F2>20,1,0))*model_coef!$F$11
        #                       + (IF(calculator!M2>=30 & calculator!M2<40,1,0))*model_coef!$F$12
        #                       + (IF(calculator!M2>=40 & calculator!M2<50,1,0))*model_coef!$F$13
        #                       + (IF(calculator!M2>=50,1,0))*model_coef!$F$14
        #                       + (calculator!B2)^2 * model_coef!$F$15
        #                       + (calculator!J2 - 25)^2 * model_coef!$F$16
        #                       + LN(IF(calculator!E2="NA",0,calculator!E2)+1) * model_coef!$F$17
        #                       + calculator!D2 * model_coef!$F$18
        #                   )

        # calculator!C2*model_coef!$F$4
        y = self.gender * ConstantTables.model_coef_F[4]

        # + (IF(calculator!G2=1,1,0))*model_coef!$F$5
        if self.race == 1:
            y += ConstantTables.model_coef_F[5]

        # + (IF(calculator!G2=2,1,0))*model_coef!$F$6
        if self.race == 2:
            y += ConstantTables.model_coef_F[6]

        # + (IF(calculator!G2=3,1,0))*model_coef!$F$7
        if self.race == 3:
            y += ConstantTables.model_coef_F[7]

        # + calculator!K2*model_coef!$F$8
        y += self.edu6 * ConstantTables.model_coef_F[8]

        #  + calculator!H2*model_coef!$F$9
        y += self.emp * ConstantTables.model_coef_F[9]

        # + (IF(calculator!J2<=18.5,1,0))*model_coef!$F$10
        if self.bmi <= 18.5:
            y += ConstantTables.model_coef_F[10]

        # + (IF(calculator!F2>20,1,0))*model_coef!$F$11
        if self.cpd > 20:
            y += ConstantTables.model_coef_F[11]

        # + (IF(calculator!M2>=30 & calculator!M2<40,1,0))*model_coef!$F$12
        if 30 <= self.pkyr_cat < 40:
            y += ConstantTables.model_coef_F[12]

        # + (IF(calculator!M2>=40 & calculator!M2<50,1,0))*model_coef!$F$13
        if 40 <= self.pkyr_cat < 50:
            y += ConstantTables.model_coef_F[13]

        #  + (IF(calculator!M2>=50,1,0))*model_coef!$F$14
        if self.pkyr_cat >= 50:
            y += ConstantTables.model_coef_F[14]

        #  + (calculator!B2)^2 * model_coef!$F$15
        y += self.age ** 2 * ConstantTables.model_coef_F[15]

        # + (calculator!J2 - 25)^2 * model_coef!$F$16
        y += (self.bmi - 25) ** 2 * ConstantTables.model_coef_F[16]

        # + LN(IF(calculator!E2="NA",0,calculator!E2)+1) * model_coef!$F$17
        y += math.log(self.qtyears + 1) * ConstantTables.model_coef_F[17]

        # + calculator!D2 * model_coef!$F$18
        y += self.smkyears * ConstantTables.model_coef_F[18]

        self.cox_death_RR = math.exp(y)

        # LCRAT_13yr_risk =     SUMPRODUCT(--(basehaz!$F$5:$F$1261<=13),
        #                               (basehaz!$H$5:$H$1261)^calculator!O2,
        #                               basehaz!$G$5:$G$1261,
        #                               (basehaz!$J$5:$J$1261)^calculator!P2)
        #                       * calculator!O2
        sum_product = float(0.0)
        for i in range(0, len(ConstantTables.basehaz_G)):
            sum_product += ConstantTables.basehaz_H[i] ** self.LCRAT_RR * ConstantTables.basehaz_G[i] \
                           * (ConstantTables.basehaz_J[i] ** self.cox_death_RR)
        self.LCRAT_13yr_risk = sum_product * self.LCRAT_RR
        # print(self.LCRAT_13yr_risk)

        # LCRAT_1mon_risk = 1-(1-S2)^(1/(13*12))
        self.LCRAT_1mon_risk = 1 - (1 - self.LCRAT_13yr_risk) ** (1 / (13 * 12))

    def print_to_screen(self):
        # Print out to the console screen:  Person [1] age: 51 (Male)   smk_years: 8  qt_years: 4  cpd: 1  ...
        print("Person [{}] age: {} ({}) smk_years: {} qt_years: {} cpd: {}  ({}, {}) fam_lung_trend: {} bmi: "
              "{}  ({}) "
              .format(self.ID, self.age, Person.gender_choices[self.gender], self.smkyears, self.qtyears,
                      self.cpd, Person.race_choices[self.race], Person.emp_choices[self.emp],
                      Person.fam_lung_trend_choices[self.fam_lung_trend], self.bmi,
                      Person.edu6_choices[self.edu6 - 1]))

    def get_years_remain_no_screening(self, progress=None, root_=None, display_progress=True):
        return get_years_remain_no_screening(self, progress, root_, display_progress)


if __name__ == "__main__":
    pass
