"""
the main startup GUI for the Lung Cancer Micro-Simulation program

Author: Phong Nguyen (vietphong.nguyen@gmail.com)
Last modified: SEP 2019
"""
from Main import Main
from MenuBar import MenuBar
from NavigationBar import NavigationBar
from Person import get_model_coef_from_file, get_basehaz_from_file
from StatusBar import StatusBar
from ToolBar import ToolBar
from read_LC_table_from_file import read_LC_table_from_file
from read_distant_cancer_table_from_file import read_distant_cancer_table_from_file
from read_life_table_from_file import read_life_table_from_file
from read_regional_cancer_table_from_file import read_regional_cancer_table_from_file

try:
    # Python3
    import tkinter as tk
except ImportError:
    # Python2
    import Tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        LC_result = None

        old_age_choice = None
        old_gender_choices = None
        old_smk_years_choices = None
        old_qt_years_choices = None
        old_cpd_choices = None
        old_race_choices = None
        old_emp_choices = None
        old_flt_choices = None
        old_bmi_entry = None
        old_edu6_choices = None

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

        self.memubar = MenuBar(parent)
        self.statusbar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.navbar = NavigationBar(self)
        self.main = Main(root)

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)

    def set_new_changing_state(p):
        global old_age_choice, old_gender_choices, old_smk_years_choices, old_qt_years_choices, old_cpd_choices, \
            old_race_choices, old_emp_choices, old_flt_choices, old_bmi_entry, old_edu6_choices

        old_age_choice = p.age
        old_gender_choices = p.gender
        old_smk_years_choices = p.smkyears
        old_qt_years_choices = p.qtyears
        old_cpd_choices = p.cpd
        old_race_choices = p.race
        old_emp_choices = p.emp
        old_flt_choices = p.fam_lung_trend
        old_bmi_entry = p.bmi
        old_edu6_choices = p.edu6


def main():
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
