from gui.models.user_config_form import UserConfigModel
from gui.views.user_config_form import UserConfigView
from collections import namedtuple
import tkinter as tk

from analysis.database_utils import get_fav_id

Numbers = namedtuple("Numbers", ["elements", "solvent"])

class UserConfigController:
    def __init__(self, parent):
        self.view = UserConfigView(parent, self)
        self.model = UserConfigModel()

    def show_error(self, title, message):
        tk.messagebox.showerror(title, message)

    def fraction_test(self, data, list, type_name):
        for element in data:
            try:
                fraction = float(element['fraction'])
            except ValueError:
                self.show_error(title = "error", message = "Fraction must be a float number")
                return

            if type_name == 'anion':
                list['anions'] += fraction
            else:
                solvent_type = element[f'{type_name}']
                list[solvent_type] += fraction

        for type, total in list.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                self.show_error(title = "error", message =f"Total fraction for {type} must be 1")
                return

    def handle_main_submit(self, name_fav, notes_fav, solvents_data, cations_data,
                           anions_data, k_factors_data, solution_info, id_phase):
        solvent_fractions = {'solvent': 0, 'antisolvent': 0}
        self.fraction_test(solvents_data, solvent_fractions, 'solvent_type')
        cation_fractions = {'a_site': 0, 'b_site': 0, 'b_double': 0, 'spacer': 0}
        self.fraction_test(cations_data, cation_fractions, 'structure_type')
        anions_fractions = {'anions': 0}
        self.fraction_test(anions_data, anions_fractions, 'anion')

        try:
            v_solvent = float(solution_info['v_solvent'])
            c_solvent = float(solution_info['c_solvent'])
            v_antisolvent = float(solution_info['v_antisolvent'])
        except ValueError:
            self.show_error(title = "error", message ="Характеристики раствора должны принимать численные значения")
            return

        for element in k_factors_data:
            try:
                k_factor = float(element['k_factor'])
            except ValueError:
                self.show_error(title = "error", message ="k-факторы должны принимать числовые значения")
                return

        v_sol = solution_info["v_solvent"]
        v_antisol = solution_info["v_antisolvent"]
        c_sol = solution_info["c_solvent"]

        self.model.add_favorite_composition(name_fav, id_phase, notes_fav, v_sol, v_antisol, c_sol)
        id_fav = get_fav_id(name_fav)

        for factor in k_factors_data:
            success, message = self.model.add_k_factors(
                id_fav,
                factor['salt'],
                factor['k_factor']
            )
            if not success:
                self.show_error(title = "error", message =message)
                return

        for solvent in solvents_data:
            success, message = self.model.add_solvent(
                id_fav,
                solvent['solvent_type'],
                solvent['symbol'],
                float(solvent['fraction'])
            )
            if not success:
                self.show_error(title = "error", message =message)
                return

        for element in cations_data:
            success, message = self.model.add_structure(
                id_fav,
                element['structure_type'],
                element['symbol'],
                float(element['fraction']),
                int(element['valence'])
            )
            if not success:
                self.show_error(title = "error", message =message)
                return

        for element in anions_data:
            success, message = self.model.add_structure(
                id_fav,
                "anion",
                element['symbol'],
                float(element['fraction']),
                1.0
            )
            if not success:
                self.show_error(title = "error", message =message)
                return
