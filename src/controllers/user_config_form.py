from src.models.user_config_form import UserConfigModel
from src.views.user_config_form import UserConfigView
from collections import namedtuple
from src.language.manager import localization_manager
from src.utils.calculation_tests import show_error

from src.utils.database_utils import get_fav_id

Numbers = namedtuple("Numbers", ["elements", "solvent"])

class UserConfigController:
    def __init__(self, parent):
        self.view = UserConfigView(parent, self)
        self.model = UserConfigModel()
        localization_manager.register_observer(self)

    def fraction_test(self, data, list, type_name):
        for element in data:
            try:
                fraction = float(element['fraction'])
            except ValueError:
                show_error(localization_manager.tr("comp_err2"))
                return

            if type_name == 'anion':
                list['anions'] += fraction
            else:
                type = element[f'{type_name}']
                list[type] += fraction

        for type, total in list.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                er1 = localization_manager.tr("comp_err31")
                er2 = localization_manager.tr("comp_err32")
                show_error(f"{er1} {type} {er2}")
                return

    def handle_main_submit(self, name_fav, notes_fav, solvents_data, cations_data,
                           anions_data, k_factors_data, solution_info, id_phase, upd=False, id_fav=None):

        if upd:
            v_sol = solution_info[2]
            v_antisol = solution_info[1]
            c_sol = solution_info[3]
        else:
            v_sol = solution_info["v_solvent"]
            v_antisol = solution_info["v_antisolvent"]
            c_sol = solution_info["c_solvent"]

        self.model.add_favorite_composition(name_fav, id_phase, notes_fav, v_sol, v_antisol, c_sol, upd, id_fav)
        id_fav = get_fav_id(name_fav)

        upd_k = upd
        for factor in k_factors_data:
            success, message = self.model.add_k_factors(
                id_fav,
                factor['salt'],
                factor['k_factor'],
                upd_k
            )
            upd_k = False
            if not success:
                show_error(message)
                return

        upd_sol = upd
        for solvent in solvents_data:
            success, message = self.model.add_solvent(
                id_fav,
                solvent['solvent_type'],
                solvent['symbol'],
                float(solvent['fraction']),
                upd_sol
            )
            upd_sol = False
            if not success:
                show_error(message)
                return

        upd_el = upd
        for element in cations_data:
            success, message = self.model.add_structure(
                id_fav,
                element['structure_type'],
                element['symbol'],
                float(element['fraction']),
                int(element['valence']),
                upd_el
            )
            upd_el = False
            if not success:
                show_error(message)
                return

        for element in anions_data:
            success, message = self.model.add_structure(
                id_fav,
                "anion",
                element['symbol'],
                float(element['fraction']),
                1.0,
                upd_el
            )
            if not success:
                show_error(message)
                return
