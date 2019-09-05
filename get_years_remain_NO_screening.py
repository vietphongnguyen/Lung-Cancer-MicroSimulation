from person import Person
from read_LC_table_from_file import read_LC_table_from_file
from read_distant_cancer_table_from_file import read_distant_cancer_table_from_file
from read_life_table_from_file import read_life_table_from_file
from read_regional_cancer_table_from_file import read_regional_cancer_table_from_file


def get_years_remain(p, life_table, LC_table, regional_LC_table, distant_LC_table, display_progress = True):
    """ Returns the total years remain - NO screening """
    print("Getting Years Remain. Please wait ...", end="")
    remain = 0
    disease_free = 1
    local_LC, regional_LC, distant_LC = [], [], []
    death_LC, death_other_causes = 0, 0

    # when calculating the a_column for constant a value: p.race consider =3 for all other races
    a_column = int((3 if p.race > 3 else p.race) * (p.gender + 1) + p.gender)

    # b	Incidence of lung cancer by age, sex, race. Lung cancer risk model-LCRAT
    b = p.LCRAT_1mon_risk
    c = 0.33  # Proportion of local cancers given no screening
    d = 0.14  # Proportion of regional cancers given no screening

    running_age = float(p.age)  # running age will increase after every loop (+ 1 month) until it reaches 100 (dead)

    total_month = (100 - p.age) * 12    # for calculating the remaining time
    display_dot = 100
    unit = 0
    current_month = 1

    while running_age < 100:
        if display_progress:
            if (current_month / total_month) > (unit / display_dot):
                print('.', end='', flush=True)
                unit += 1
            current_month += 1

        # Constant a. Age-, sex-, and race/ethnicity-specific prob. of dying from life table.
        # See Sheet "Life-table", column K to R. This is per month prob
        a = life_table[int(running_age) - 50][a_column]

        # disease_free
        disease_free_death_other_causes = a * disease_free
        death_other_causes += disease_free_death_other_causes
        disease_free_survive = disease_free - disease_free_death_other_causes
        disease_free_survive_LC = disease_free_survive * b
        disease_free_survive_No_LC = disease_free_survive - disease_free_survive_LC
        disease_free_survive_LC_local_LC = disease_free_survive_LC * c
        disease_free_survive_LC_regional_LC = disease_free_survive_LC * d
        disease_free_survive_LC_distant_LC = disease_free_survive_LC - disease_free_survive_LC_local_LC - disease_free_survive_LC_regional_LC
        remain += disease_free_survive

        # Sum up for the next loop
        disease_free = disease_free_survive_No_LC
        local_LC.append([disease_free_survive_LC_local_LC, 0])  # add local_LC with interval = 0 month
        regional_LC.append([disease_free_survive_LC_regional_LC, 0])
        distant_LC.append([disease_free_survive_LC_distant_LC, 0])

        # local_LC
        for i in range(len(local_LC)):
            if local_LC[i][1] >= 1:  # if the interval time from 1 month
                local_LC_death_other_causes = local_LC[i][0] * a
                death_other_causes += local_LC_death_other_causes
                local_LC_survive = local_LC[i][0] - local_LC_death_other_causes

                # e: Prob of transition from local to distant cancer
                # = 1-'Survival rate-Local cancer'!columnF*(1-'Life-table'!columnK-R)
                # "See Sheet ""Survival rate-Local cancer""
                # We assumed death rate by cancer stage represents the transition from local/regional to distant cancer because pts die from distant cancer only.
                # Survival estimate from SEER data, by time since diagnosis in months, age (20-39, 40-49, 50-59, 60-69, 70-79, >=80 y), sex, race/ethnicity"

                interval = local_LC[i][1] - 1
                if interval > 119: interval = 119
                age = int(running_age / 10 - 4)
                if age > 4: age = 4
                # print(interval, p.gender, p.race, age)
                e = 1 - LC_table[interval][p.gender][p.race][age] * (1 - a)
                local_LC_survive_distant_LC = local_LC_survive * e
                distant_LC.append([local_LC_survive_distant_LC, 0])  # initial with interval = 0 month
                local_LC_survive -= local_LC_survive_distant_LC
                local_LC[i][0] = local_LC_survive
            local_LC[i][1] += 1  # increase the interval by 1 month

        # regional_LC
        for i in range(len(regional_LC)):
            if regional_LC[i][1] >= 1:  # if the interval time from 1 month
                regional_LC_death_other_causes = regional_LC[i][0] * a
                death_other_causes += regional_LC_death_other_causes
                regional_LC_survive = regional_LC[i][0] - regional_LC_death_other_causes

                # f: Prob of transition from regional to distant cancer
                # = 1-'Survival rate-Regional cancer'!columnF*(1-'Life-table'!columnK-R)

                interval = regional_LC[i][1] - 1
                if interval > 119: interval = 119
                age = int(running_age / 10 - 4)
                if age > 4: age = 4
                # print(interval, p.gender, p.race, age)
                f = 1 - regional_LC_table[interval][p.gender][p.race][age] * (1 - a)
                regional_LC_survive_distant_LC = regional_LC_survive * f
                distant_LC.append([regional_LC_survive_distant_LC, 0])  # initial with interval = 0 month
                regional_LC_survive -= regional_LC_survive_distant_LC
                regional_LC[i][0] = regional_LC_survive
            regional_LC[i][1] += 1  # increase the interval by 1 month

        # distant_LC
        for i in range(len(distant_LC)):
            if distant_LC[i][1] >= 1:  # if the interval time from 1 month
                distant_LC_death_other_causes = distant_LC[i][0] * a
                death_other_causes += distant_LC_death_other_causes
                distant_LC_survive = distant_LC[i][0] - distant_LC_death_other_causes

                # g: Prob. of dying from distant cancer
                # = 1-'Survival rate-Distant cancer'!columnF*(1-'Life-table'!columnK-R)

                interval = distant_LC[i][1] - 1
                if interval > 119: interval = 119
                age = int(running_age / 10 - 4)
                if age > 4: age = 4
                # print(interval, p.gender, p.race, age)
                g = 1 - distant_LC_table[interval][p.gender][p.race][age] * (1 - a)
                distant_LC_survive_die = distant_LC_survive * g

                distant_LC_survive -= distant_LC_survive_die
                distant_LC[i][0] = distant_LC_survive
            distant_LC[i][1] += 1  # increase the interval by 1 month

        running_age += 1 / 12  # increase age by a month

    print("done")
    return remain / 12  # remain increased every loop (every month). Have to return in years by dividing by 12


def test():
    # init reading data table
    life_table1 = read_life_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    local_cancer2 = read_LC_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    regional_cancer3 = read_regional_cancer_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    distant_cancer4 = read_distant_cancer_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")

    p1 = Person(72, 1, 42, 6, 24, 2, 0, 2, 27, 5, 50.4, 0.000983915, 4)
    p2 = Person(80, 0, 0, 0, 0, 0, 0, 0, 24.62, 0)
    print(get_years_remain(p2, life_table1, local_cancer2, regional_cancer3, distant_cancer4, False))


# test()
