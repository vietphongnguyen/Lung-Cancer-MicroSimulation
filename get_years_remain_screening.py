from Person import Person, get_basehaz_from_file, get_model_coef_from_file
from read_LC_table_from_file import read_LC_table_from_file
from read_distant_cancer_table_from_file import read_distant_cancer_table_from_file
from read_life_table_from_file import read_life_table_from_file
from read_people_from_file import read_people_from_file
from read_regional_cancer_table_from_file import read_regional_cancer_table_from_file


def get_years_remain_screening(p, life_table, LC_table, regional_LC_table, distant_LC_table, progress=None, root=None,
                               display_progress=True):
    """ Returns the total years remain - with Screening Option """
    print("Peron [" + p.ID + "] : Getting Years Remain (with Screening Option). Please wait ...", end="")
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

    total_month = (100 - p.age) * 12  # for calculating the remaining time
    display_dot = 100
    unit = 0
    current_month = 1

    try:
        progress['style'] = "red.Horizontal.TProgressbar"
    except TypeError:
        pass
    due_screen = 12  # initiate the due screen = 12 month so that they need to do screening immediately
    sen = 0.6448  # sen : Sensitivity of CT = 0.6448 (From USPSTF's model)
    first_screening = True  # first round of screening
    p = 0.10540954  # p: Prob. of having an invasive procedure with or without a noninvasive procedure
    # p = 0.10540954 (Based on table 3, Aberle DR 2011)
    q1 = 0.415  # q1	Prob of Chest Radiography after positive CT	0.415
    # (This is different for round of screening, but for now, we will use the value of round 0)
    q2 = 0.67  # q2	Prob of Chest CT after positive CT	0.67
    q3 = 0.633  # q3	Prob of FDG-PET or FDG-PET and CT after positive CT	0.633
    sum_q = q1 + q2 + q3  # because the sum q1+q2+q3 is greater than 100% -> We normalize the value of q. ??????
    q1 /= sum_q  # For now, we just consider the patient will do only one of those tests (not combine):
    q2 /= sum_q  # Chest Radiography, Chest CT, FDG-PET or FDG-PET and CT
    q3 /= sum_q

    m1 = 0.02173913  # m1	Prob of dying after noninvasive procedure	0.02173913
    m2 = 0.02173913  # m2	Prob of dying after noninvasive procedure	0.02173913
    m3 = 0.02173913  # m3	Prob of dying after noninvasive procedure	0.02173913

    # s1	Prob of complications after noninvasive procedure	0.1304
    # s2	Prob of complications after noninvasive procedure	0.1304
    # s3	Prob of complications after noninvasive procedure	0.1304
    s123 = 0.1304

    k = 0.67  # k	Proportion of local cancers given positive screening	0.67
    l = 0.12  # l	Proportion of regional cancers given positive screening	0.12

    q4 = 0.363  # q4	Prob of Percutaneous cytologic analysis or biopsy after postive CT	0.363
    q5 = 0.585  # q5	Prob of Bronchoscopy after postive CT	0.585
    q6 = 0.178  # q6	Prob of Mediastinoscopy or mediastinotomy after postive CT	0.178
    q7 = 0.163  # q7	Prob of Thoracoscopy after postive CT	0.163
    q8 = 0.578  # q8	Prob of Thoracotomy after postive CT	0.578
    sum_q = q4 + q5 + q6 + q7 + q8  # because the sum q4-8 is greater than 100% -> We normalize the value of q. ??????
    q4 /= sum_q  # For now, we just consider the patient will do only one of those tests (not combine):
    q5 /= sum_q  # Percutaneous, Bronchoscopy, Mediastinoscopy, Thoracoscopy, Thoracotomy
    q6 /= sum_q
    q7 /= sum_q
    q8 /= sum_q

    m4 = 0.032258065  # m4	Prob of dying after percutaneous cytologic analysis or biopsy	0.032258065
    m5 = 0.073770492  # m5	Prob of dying after bronchoscopy	0.073770492
    m678 = 0.012893983  # m6	Prob of dying after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy	0.012893983
    # m7	Prob of dying after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy	0.012893983
    # m8	Prob of dying after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy	0.012893983

    s4 = 0.129  # s4	Prob of complications after percutaneous cytologic analysis or biopsy	0.129
    s5 = 0.0902  # s5	Prob of complications after bronchoscopy	0.0902
    # s6	Prob of complications after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy	0.3209
    # s7	Prob of complications after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy	0.3209
    # s8	Prob of complications after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy	0.3209
    s678 = 0.3209

    ii = 0.20  # ii	Proportion of local cancers given negative screening	0.20
    jj = 0.14  # jj	Proportion of regional cancers given negative screening	0.14

    spec = 0.734  # spec	Specificity of CT	0.734

    q1_2 = 0.192  # q1_2	Prob of Chest Radiography after negative CT	0.192
    # This is different for round of screening, but for now, we will use the value of round 0
    q2_2 = 0.815  # q2_2	Prob of Chest CT after negative CT	0.815
    q3_2 = 0.091  # q3_2	Prob of FDG-PET or FDG-PET and CT after negative CT	0.091
    sum_q = q1_2 + q2_2 + q3_2  # because the sum q1+q2+q3 is greater than 100% -> We normalize the value of q. ??????
    q1_2 /= sum_q  # For now, we just consider the patient will do only one of those tests (not combine):
    q2_2 /= sum_q  # Chest Radiography, Chest CT, FDG-PET or FDG-PET and CT
    q3_2 /= sum_q

    q4_2 = 0.009  # q4_2	Prob of Percutaneous cytologic analysis or biopsy after negative CT	0.009
    q5_2 = 0.024  # q5_2	Prob of Bronchoscopy after negative CT	0.024
    q6_2 = 0.002  # q6_2	Prob of Mediastinoscopy or mediastinotomy after negative CT	0.002
    q7_2 = 0.006  # q7_2	Prob of Thoracoscopy after negative CT	0.006
    q8_2 = 0.007  # q8_2	Prob of Thoracotomy after negative CT	0.007
    sum_q = q4_2 + q5_2 + q6_2 + q7_2 + q8_2  # because the sum q4-8 is greater than 100% -> We normalize the value of q. ??????
    q4_2 /= sum_q  # For now, we just consider the patient will do only one of those tests (not combine):
    q5_2 /= sum_q  # Percutaneous, Bronchoscopy, Mediastinoscopy, Thoracoscopy, Thoracotomy
    q6_2 /= sum_q
    q7_2 /= sum_q
    q8_2 /= sum_q

    # m1_2	Prob of dying after noninvasive procedure following negative CT	0.000378161
    # m2_2	Prob of dying after noninvasive procedure following negative CT	0.000378161
    # m3_2	Prob of dying after noninvasive procedure following negative CT	0.000378161
    m123_2 = 0.000378161
    # m4_2	Prob of dying after percutaneous cytologic analysis or biopsy following negative CT	0
    m5_2 = 0.014652015  # m5_2	Prob of dying after bronchoscopy following negative CT	0.014652015
    # m6_2	Prob of dying after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy following negative CT	0.00286533
    # m7_2	Prob of dying after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy following negative CT	0.00286533
    # m8_2	Prob of dying after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy following negative CT	0.00286533
    m678_2 = 0.00286533

    # s1_2	Prob of complications after noninvasive procedure following negative CT	0.0012
    # s2_2	Prob of complications after noninvasive procedure following negative CT	0.0012
    # s3_2	Prob of complications after noninvasive procedure following negative CT	0.0012
    s123_2 = 0.0012
    # s4_2	Prob of complications after percutaneous cytologic analysis or biopsy following negative CT	0
    # s5_2	Prob of complications after bronchoscopy following negative CT	0
    # s6_2	Prob of complications after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy following negative CT	0.0472
    # s7_2	Prob of complications after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy following negative CT	0.0472
    # s8_2	Prob of complications after thoracoscopy/thoracotomy or mediastinoscopy/mediastinotomy following negative CT	0.0472
    s678_2 = 0.0472

    while running_age < 100:
        # update the progress bar in gui2
        try:
            progress['value'] = (running_age - 50) ** 2 / 25
            root.update_idletasks()
        except TypeError:
            pass

        if display_progress:
            if (current_month / total_month) > (unit / display_dot):
                print('.', end='', flush=True)
                unit += 1
            current_month += 1

        # Constant a. Age-, sex-, and race/ethnicity-specific prob. of dying from life table.
        # See Sheet "Life-table", column K to R. This is per month prob
        # print("int(running_age) - 50 = " + str(int(running_age) - 50) + " | a_column = " + str(a_column))
        a = life_table[int(running_age) - 50][a_column]

        # disease_free
        disease_free_death_other_causes = a * disease_free
        death_other_causes += disease_free_death_other_causes
        disease_free_survive = disease_free - disease_free_death_other_causes

        disease_free_survive_LC = disease_free_survive * b
        disease_free_survive_No_LC = disease_free_survive - disease_free_survive_LC

        # Now is the screening involve
        if due_screen >= 12:  # if due screen every year (12 months)
            # CT (+) = sen
            CT_true = disease_free_survive_LC * sen
            CT_false = disease_free_survive_LC - CT_true  # CT (-)

            # n : Prob. of receiving diagnosis procedure after CT(+). if(first round of screening=1,0.904,0.574)
            if first_screening:
                n = 0.904
                first_screening = False
            else:
                n = 0.574
            diagnostic_follow_up = CT_true * n
            no_follow_up = CT_true - diagnostic_follow_up

            invasive_procedure = diagnostic_follow_up * p
            noninvasive_procedure_only = diagnostic_follow_up - invasive_procedure

            chest_radiography = noninvasive_procedure_only * q1
            chest_CT = noninvasive_procedure_only * q2
            PET_and_CT = noninvasive_procedure_only * q3  # FDG - PET or FDG - PET and CT

            chest_radiography_die_after_procedure = chest_radiography * m1
            chest_radiography_survive = chest_radiography - chest_radiography_die_after_procedure
            chest_radiography_complications = chest_radiography_survive * s123
            chest_radiography_no_complications = chest_radiography_survive - chest_radiography_complications
            chest_radiography_complications_local_LC = chest_radiography_complications * k
            chest_radiography_complications_regional_LC = chest_radiography_complications * l
            chest_radiography_complications_distant_LC = chest_radiography_complications \
                                                         - chest_radiography_complications_local_LC \
                                                         - chest_radiography_complications_regional_LC
            chest_radiography_no_complications_local_LC = chest_radiography_no_complications * k
            chest_radiography_no_complications_regional_LC = chest_radiography_no_complications * l
            chest_radiography_no_complications_distant_LC = chest_radiography_no_complications \
                                                            - chest_radiography_no_complications_local_LC \
                                                            - chest_radiography_no_complications_regional_LC

            chest_CT_die_after_procedure = chest_CT * m2
            chest_CT_survive = chest_CT - chest_CT_die_after_procedure
            chest_CT_complications = chest_CT_survive * s123
            chest_CT_no_complications = chest_CT_survive - chest_CT_complications
            chest_CT_complications_local_LC = chest_CT_complications * k
            chest_CT_complications_regional_LC = chest_CT_complications * l
            chest_CT_complications_distant_LC = chest_CT_complications \
                                                - chest_CT_complications_local_LC \
                                                - chest_CT_complications_regional_LC
            chest_CT_no_complications_local_LC = chest_CT_no_complications * k
            chest_CT_no_complications_regional_LC = chest_CT_no_complications * l
            chest_CT_no_complications_distant_LC = chest_CT_no_complications \
                                                   - chest_CT_no_complications_local_LC \
                                                   - chest_CT_no_complications_regional_LC

            PET_and_CT_die_after_procedure = PET_and_CT * m3
            PET_and_CT_survive = PET_and_CT - PET_and_CT_die_after_procedure
            PET_and_CT_complications = PET_and_CT_survive * s123
            PET_and_CT_no_complications = PET_and_CT_survive - PET_and_CT_complications
            PET_and_CT_complications_local_LC = PET_and_CT_complications * k
            PET_and_CT_complications_regional_LC = PET_and_CT_complications * l
            PET_and_CT_complications_distant_LC = PET_and_CT_complications \
                                                  - PET_and_CT_complications_local_LC \
                                                  - PET_and_CT_complications_regional_LC
            PET_and_CT_no_complications_local_LC = PET_and_CT_no_complications * k
            PET_and_CT_no_complications_regional_LC = PET_and_CT_no_complications * l
            PET_and_CT_no_complications_distant_LC = PET_and_CT_no_complications \
                                                     - PET_and_CT_no_complications_local_LC \
                                                     - PET_and_CT_no_complications_regional_LC

            percutaneous = invasive_procedure * q4
            bronchoscopy = invasive_procedure * q5
            mediastinoscopy = invasive_procedure * q6
            thoracoscopy = invasive_procedure * q7
            thoracotomy = invasive_procedure * q8

            percutaneous_die_after_procedure = percutaneous * m4
            percutaneous_survive = percutaneous - percutaneous_die_after_procedure
            percutaneous_complications = percutaneous_survive * s4
            percutaneous_no_complications = percutaneous_survive - percutaneous_complications
            percutaneous_complications_local_LC = percutaneous_complications * k
            percutaneous_complications_regional_LC = percutaneous_complications * l
            percutaneous_complications_distant_LC = percutaneous_complications \
                                                    - percutaneous_complications_local_LC \
                                                    - percutaneous_complications_regional_LC
            percutaneous_no_complications_local_LC = percutaneous_no_complications * k
            percutaneous_no_complications_regional_LC = percutaneous_no_complications * l
            percutaneous_no_complications_distant_LC = percutaneous_no_complications \
                                                       - percutaneous_no_complications_local_LC \
                                                       - percutaneous_no_complications_regional_LC

            bronchoscopy_die_after_procedure = bronchoscopy * m5
            bronchoscopy_survive = bronchoscopy - bronchoscopy_die_after_procedure
            bronchoscopy_complications = bronchoscopy_survive * s5
            bronchoscopy_no_complications = bronchoscopy_survive - bronchoscopy_complications
            bronchoscopy_complications_local_LC = bronchoscopy_complications * k
            bronchoscopy_complications_regional_LC = bronchoscopy_complications * l
            bronchoscopy_complications_distant_LC = bronchoscopy_complications \
                                                    - bronchoscopy_complications_local_LC \
                                                    - bronchoscopy_complications_regional_LC
            bronchoscopy_no_complications_local_LC = bronchoscopy_no_complications * k
            bronchoscopy_no_complications_regional_LC = bronchoscopy_no_complications * l
            bronchoscopy_no_complications_distant_LC = bronchoscopy_no_complications \
                                                       - bronchoscopy_no_complications_local_LC \
                                                       - bronchoscopy_no_complications_regional_LC

            mediastinoscopy_die_after_procedure = mediastinoscopy * m678
            mediastinoscopy_survive = mediastinoscopy - mediastinoscopy_die_after_procedure
            mediastinoscopy_complications = mediastinoscopy_survive * s678
            mediastinoscopy_no_complications = mediastinoscopy_survive - mediastinoscopy_complications
            mediastinoscopy_complications_local_LC = mediastinoscopy_complications * k
            mediastinoscopy_complications_regional_LC = mediastinoscopy_complications * l
            mediastinoscopy_complications_distant_LC = mediastinoscopy_complications \
                                                       - mediastinoscopy_complications_local_LC \
                                                       - mediastinoscopy_complications_regional_LC
            mediastinoscopy_no_complications_local_LC = mediastinoscopy_no_complications * k
            mediastinoscopy_no_complications_regional_LC = mediastinoscopy_no_complications * l
            mediastinoscopy_no_complications_distant_LC = mediastinoscopy_no_complications \
                                                          - mediastinoscopy_no_complications_local_LC \
                                                          - mediastinoscopy_no_complications_regional_LC

            thoracoscopy_die_after_procedure = thoracoscopy * m678
            thoracoscopy_survive = thoracoscopy - thoracoscopy_die_after_procedure
            thoracoscopy_complications = thoracoscopy_survive * s678
            thoracoscopy_no_complications = thoracoscopy_survive - thoracoscopy_complications
            thoracoscopy_complications_local_LC = thoracoscopy_complications * k
            thoracoscopy_complications_regional_LC = thoracoscopy_complications * l
            thoracoscopy_complications_distant_LC = thoracoscopy_complications \
                                                    - thoracoscopy_complications_local_LC \
                                                    - thoracoscopy_complications_regional_LC
            thoracoscopy_no_complications_local_LC = thoracoscopy_no_complications * k
            thoracoscopy_no_complications_regional_LC = thoracoscopy_no_complications * l
            thoracoscopy_no_complications_distant_LC = thoracoscopy_no_complications \
                                                       - thoracoscopy_no_complications_local_LC \
                                                       - thoracoscopy_no_complications_regional_LC

            thoracotomy_die_after_procedure = thoracotomy * m678
            thoracotomy_survive = thoracotomy - thoracotomy_die_after_procedure
            thoracotomy_complications = thoracotomy_survive * s678
            thoracotomy_no_complications = thoracotomy_survive - thoracotomy_complications
            thoracotomy_complications_local_LC = thoracotomy_complications * k
            thoracotomy_complications_regional_LC = thoracotomy_complications * l
            thoracotomy_complications_distant_LC = thoracotomy_complications \
                                                   - thoracotomy_complications_local_LC \
                                                   - thoracotomy_complications_regional_LC
            thoracotomy_no_complications_local_LC = thoracotomy_no_complications * k
            thoracotomy_no_complications_regional_LC = thoracotomy_no_complications * l
            thoracotomy_no_complications_distant_LC = thoracotomy_no_complications \
                                                      - thoracotomy_no_complications_local_LC \
                                                      - thoracotomy_no_complications_regional_LC

            no_follow_up_local_LC = no_follow_up * k
            no_follow_up_regional_LC = no_follow_up * l
            no_follow_up_distant_LC = no_follow_up - no_follow_up_local_LC - no_follow_up_regional_LC

            CT_false_local_LC = CT_false * ii
            CT_false_regional_LC = CT_false * jj
            CT_false_distant_LC = CT_false - CT_false_local_LC - CT_false_regional_LC

            # #######################################################################################################

            # No_LC : CT (-) = spec
            No_LC_CT_false = disease_free_survive_No_LC * spec
            No_LC_CT_true = disease_free_survive_No_LC - No_LC_CT_false  # CT (+)

            diagnostic_follow_up = No_LC_CT_true * n
            no_follow_up = No_LC_CT_true - diagnostic_follow_up
            invasive_procedure = diagnostic_follow_up * p
            noninvasive_procedure_only = diagnostic_follow_up - invasive_procedure

            chest_radiography = noninvasive_procedure_only * q1_2
            chest_CT = noninvasive_procedure_only * q2_2
            PET_and_CT = noninvasive_procedure_only * q3_2  # FDG - PET or FDG - PET and CT

            chest_radiography_die_after_procedure = chest_radiography * m123_2
            chest_radiography_survive = chest_radiography - chest_radiography_die_after_procedure
            chest_radiography_complications = chest_radiography_survive * s123_2
            chest_radiography_no_complications = chest_radiography_survive - chest_radiography_complications

            chest_CT_die_after_procedure = chest_CT * m123_2
            chest_CT_survive = chest_CT - chest_CT_die_after_procedure
            chest_CT_complications = chest_CT_survive * s123_2
            chest_CT_no_complications = chest_CT_survive - chest_CT_complications

            PET_and_CT_die_after_procedure = PET_and_CT * m123_2
            PET_and_CT_survive = PET_and_CT - PET_and_CT_die_after_procedure
            PET_and_CT_complications = PET_and_CT_survive * s123_2
            PET_and_CT_no_complications = PET_and_CT_survive - PET_and_CT_complications

            percutaneous = invasive_procedure * q4_2
            bronchoscopy = invasive_procedure * q5_2
            mediastinoscopy = invasive_procedure * q6_2
            thoracoscopy = invasive_procedure * q7_2
            thoracotomy = invasive_procedure * q8_2

            # m4_2 = 0
            # percutaneous_die_after_procedure = percutaneous * m4_2
            # percutaneous_survive = percutaneous - percutaneous_die_after_procedure
            # s4_2 = 0
            # percutaneous_complications = percutaneous_survive * s4_2
            # percutaneous_no_complications = percutaneous_survive - percutaneous_complications

            bronchoscopy_die_after_procedure = bronchoscopy * m5_2
            bronchoscopy_survive = bronchoscopy - bronchoscopy_die_after_procedure
            # s5_2 = 0
            # bronchoscopy_complications = bronchoscopy_survive * s5_2
            # bronchoscopy_no_complications = bronchoscopy_survive - bronchoscopy_complications

            mediastinoscopy_die_after_procedure = mediastinoscopy * m678_2
            mediastinoscopy_survive = mediastinoscopy - mediastinoscopy_die_after_procedure
            mediastinoscopy_complications = mediastinoscopy_survive * s678_2
            mediastinoscopy_no_complications = mediastinoscopy_survive - mediastinoscopy_complications

            thoracoscopy_die_after_procedure = thoracoscopy * m678_2
            thoracoscopy_survive = thoracoscopy - thoracoscopy_die_after_procedure
            thoracoscopy_complications = thoracoscopy_survive * s678_2
            thoracoscopy_no_complications = thoracoscopy_survive - thoracoscopy_complications

            thoracotomy_die_after_procedure = thoracotomy * m678_2
            thoracotomy_survive = thoracotomy - thoracotomy_die_after_procedure
            thoracotomy_complications = thoracotomy_survive * s678_2
            thoracotomy_no_complications = thoracotomy_survive - thoracotomy_complications

            # Sum up for the next loop
            disease_free = disease_free_survive_No_LC - chest_radiography_die_after_procedure \
                           - chest_CT_die_after_procedure - PET_and_CT_die_after_procedure \
                           - bronchoscopy_die_after_procedure - mediastinoscopy_die_after_procedure \
                           - thoracoscopy_die_after_procedure - thoracotomy_die_after_procedure

            due_screen = 0

        else:  # not screen (undue)
            due_screen += 1
            LC_local_LC = disease_free_survive_LC * c
            LC_regional_LC = disease_free_survive_LC * d
            LC_distant_LC = disease_free_survive_LC - LC_local_LC - LC_regional_LC

            local_LC.append([LC_local_LC, 0])  # add local_LC with interval = 0 month
            regional_LC.append([LC_regional_LC, 0])
            distant_LC.append([LC_distant_LC, 0])

            # Sum up for the next loop
            disease_free = disease_free_survive_No_LC

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
                if age > 4:
                    age = 4
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
    try:
        progress['style'] = "green.Horizontal.TProgressbar"
        progress['value'] = progress["maximum"]
    except TypeError:
        pass

    return remain / 12  # remain increased every loop (every month). Have to return in years by dividing by 12


def test():
    # init reading data table
    life_table1 = read_life_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    local_cancer2 = read_LC_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    regional_cancer3 = read_regional_cancer_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")
    distant_cancer4 = read_distant_cancer_table_from_file("input/Copy of Lung cancer_7-19-2019.xlsx")

    p1 = Person(72, 1, 42, 6, 24, 2, 0, 2, 27, 5, 50.4, 0.000983915, 4)
    p2 = Person(80, 0, 0, 0, 0, 0, 0, 0, 24.62, 0)
    print(get_years_remain_screening(p2, life_table1, local_cancer2, regional_cancer3, distant_cancer4, False))


def test2():
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
        years_remain = get_years_remain_screening(people_list[i], life_table, local_cancer, regional_cancer,
                                                  distant_cancer, None, None, True)
        print("Years remain: " + str(years_remain) + " \n")
        total_years_remain += years_remain

    print("\n ------------------------ \nTotal life years remain: " + str(total_years_remain) + " \n")
    print("Average life years per person: " + str(total_years_remain / len(people_list)) + " \n ----------------- \n")

# test()
