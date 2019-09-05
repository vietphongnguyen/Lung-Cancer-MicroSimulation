import math

import xlrd


def get_basehaz_from_file(file_name):
    print("Reading Baseline hazard/survival array from file [" + file_name + "] ...", end="")
    table = []

    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("basehaz")
    for i in range(4, input_worksheet.nrows):
        time = float(input_worksheet.cell_value(i, 5))
        table.append(time)

    print("done")
    return table


def get_model_coef_from_file(file_name, column):
    print("Reading [model_coef] array [at column : " + str(column) + " ] from file [" + file_name + "] ...", end="")
    table = [0, 1, 2, 3]

    input_workbook = xlrd.open_workbook(file_name)
    input_worksheet = input_workbook.sheet_by_name("model_coef")
    for i in range(4, 20):
        try:
            coef = float(input_worksheet.cell_value(i-1, column))
        except ValueError:
            coef = float(0.0)
        table.append(coef)

    print("done")
    return table


class Person:

    def __init__(self, age, gender, smkyears, qtyears, cpd, race, emp, fam_lung_trend, bmi, edu6,
                 pkyr_cat=50.4, LCRAT_1mon_risk=0.000983915, ID=0):
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
        self.edu6 = edu6  # highest education level (1=<12 grade, 2=HS graduate,
        # 3=post hs/no college, 4=associate degree/some college,
        # 5=bachelors degree, 6=graduate school)
        self.pkyr_cat = pkyr_cat
        self.LCRAT_1mon_risk = LCRAT_1mon_risk  # (Constant b) 1 month risk. Incidence of lung cancer by age, sex, race.
        # Lung cancer risk model-LCRAT

    def initiate_LCRAT_1mon_risk(self, basehaz=get_basehaz_from_file("input/lcrisk_tool.xlsx")):

        print("[basehaz] table has " + str(len(basehaz)) + " items : ", end="")
        print(basehaz)

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

        model_coef_D = get_model_coef_from_file("input/lcrisk_tool.xlsx",3)
        print(model_coef_D)

        # calculator!C2 * model_coef!$D$4
        x = self.gender * model_coef_D[4]

        # +(IF(calculator!G2=1,1,0))*model_coef!$D$5
        if self.race == 1:
            x += model_coef_D[5]

        # +(IF(calculator!G2=2,1,0))*model_coef!$D$6
        if self.race == 2:
            x += model_coef_D[6]

        # +(IF(calculator!G2=3,1,0))*model_coef!$D$7
        if self.race == 3:
            x += model_coef_D[7]

        # +calculator!K2*model_coef!$D$8
        x += self.edu6 * model_coef_D[8]

        #  +calculator!I2*model_coef!$D$9
        x += self.fam_lung_trend * model_coef_D[9]

        # +calculator!H2*model_coef!$D$10
        x += self.emp * model_coef_D[10]

        # +(IF(calculator!J2<=18.5,1,0))*model_coef!$D$11
        if self.bmi <= 18.5:
            x += model_coef_D[11]

        # +(IF(calculator!F2>20,1,0))*model_coef!$D$12
        if self.cpd > 20:
            x += model_coef_D[12]

        # +(IF(calculator!M2>=30 & calculator!M2<40,1,0))*model_coef!$D$13
        self.pkyr_cat = self.smkyears * self.cpd / 20  # pkyr_cat = D2 * F2 / 20
        if 30 <= self.pkyr_cat < 40:
            x += model_coef_D[13]

        # +(IF(calculator!M2>=40 & calculator!M2<50,1,0))*model_coef!$D$14
        if 40 <= self.pkyr_cat < 50:
            x += model_coef_D[14]

        # +(IF(calculator!M2>=50,1,0))*model_coef!$D$15
        if self.pkyr_cat >= 50:
            x += model_coef_D[15]

        #  +LN(calculator!B2)*model_coef!$D$16
        x += math.log(self.age) * model_coef_D[16]

        #  +LN(calculator!J2)*model_coef!$D$17
        x += math.log(self.bmi) * model_coef_D[17]

        # +LN(IF(calculator!E2="NA",0,calculator!E2)+1)*model_coef!$D$18
        x += math.log(self.qtyears) * model_coef_D[18]

        # +calculator!D2*model_coef!$D$19
        x += self.smkyears * model_coef_D[19]

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

        model_coef_F = get_model_coef_from_file("input/lcrisk_tool.xlsx", 5)

        # calculator!C2*model_coef!$F$4
        y = self.gender * model_coef_F[4]

        # + (IF(calculator!G2=1,1,0))*model_coef!$F$5
        if self.race == 1:
            y += model_coef_F[5]

        # + (IF(calculator!G2=2,1,0))*model_coef!$F$6
        if self.race == 2:
            y += model_coef_F[6]

        # + (IF(calculator!G2=3,1,0))*model_coef!$F$7
        if self.race == 3:
            y += model_coef_F[7]

        # + calculator!K2*model_coef!$F$8
        y += self.edu6 * model_coef_F[8]

        #  + calculator!H2*model_coef!$F$9
        y += self.emp * model_coef_F[9]

        # + (IF(calculator!J2<=18.5,1,0))*model_coef!$F$10
        if self.bmi <= 18.5:
            y += model_coef_F[10]

        # + (IF(calculator!F2>20,1,0))*model_coef!$F$11
        if self.cpd > 20:
            y += model_coef_F[11]

        # + (IF(calculator!M2>=30 & calculator!M2<40,1,0))*model_coef!$F$12
        if 30 <= self.pkyr_cat < 40:
            y += model_coef_F[12]

        # + (IF(calculator!M2>=40 & calculator!M2<50,1,0))*model_coef!$F$13
        if 40 <= self.pkyr_cat < 50:
            y += model_coef_F[13]

        #  + (IF(calculator!M2>=50,1,0))*model_coef!$F$14
        if self.pkyr_cat >= 50:
            y += model_coef_F[14]

        #  + (calculator!B2)^2 * model_coef!$F$15
        y += self.age ** 2 * model_coef_F[15]

        # + (calculator!J2 - 25)^2 * model_coef!$F$16
        y += (self.bmi - 25) ** 2 * model_coef_F[16]

        # + LN(IF(calculator!E2="NA",0,calculator!E2)+1) * model_coef!$F$17
        y += math.log(self.qtyears + 1) * model_coef_F[17]

        # + calculator!D2 * model_coef!$F$18
        y += self.smkyears * model_coef_F[18]

        self.cox_death_RR = math.exp(y)

        print("self.LCRAT_RR = " + str(self.LCRAT_RR) + "  |  self.cox_death_RR = " + str(self.cox_death_RR))

        # LCRAT_13yr_risk =     SUMPRODUCT(--(basehaz!$F$5:$F$1261<=13),
        #                               (basehaz!$H$5:$H$1261)^calculator!O2,
        #                               basehaz!$G$5:$G$1261,
        #                               (basehaz!$J$5:$J$1261)^calculator!P2)
        #                       * calculator!O2
        sum_product = float(0.0)
        for i in basehaz:
            if i <= 13:
                sum_product += (i ** self.LCRAT_RR) * i * (i ** self.cox_death_RR)
        self.LCRAT_13yr_risk = sum_product * self.LCRAT_RR

        # LCRAT_1mon_risk = 1-(1-S2)^(1/(13*12))
        self.LCRAT_1mon_risk = 1 - (1 - self.LCRAT_13yr_risk) ^ (1 / (13 * 12))


def test_initiate_LCRAT_1mon_risk():
    p2 = Person(
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
        # 50.4,  # pkyr_cat
        # 0.000983915,  # LCRAT_1mon_risk
        # 4  # ID
    )
    p2.initiate_LCRAT_1mon_risk()

    print(p2.LCRAT_1mon_risk)


test_initiate_LCRAT_1mon_risk()


def test():
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
        50.4,  # pkyr_cat
        0.000983915,  # LCRAT_1mon_risk
        4  # ID
    )
    print(p1.age)
    print(p1.gender)
