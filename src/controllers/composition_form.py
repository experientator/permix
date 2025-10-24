from collections import namedtuple

from src.utils.database_utils import get_template_id
from src.models.composition_form import CompositionModel
from src.views.composition_form import CompositionView
from src.language.manager import localization_manager
from src.utils.calculation_tests import show_error, show_success

Numbers = namedtuple("Numbers", ["elements", "solvent"])

class CompositionController:
    def __init__(self, parent):
        self.model = CompositionModel()
        self.view = CompositionView(parent, self)
        localization_manager.register_observer(self)

    def handle_main_submit(self, main_data,  solution_info, structure_data,
                           solvent_data, properties_data, factors_data, upd = False, id_info = None):

        device_type = self.view.entry_device_type.get()

        solvent_fractions = {'solvent': 0, 'antisolvent': 0}
        for solvent in solvent_data:
            try:
                fraction = float(solvent['fraction'])
            except ValueError:
                show_error(localization_manager.tr("comp_err2"))
                return

            solvent_type = solvent['solvent_type']
            solvent_fractions[solvent_type] += fraction

        for stype, total in solvent_fractions.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                er1 = localization_manager.tr("comp_err31")
                er2 = localization_manager.tr("comp_err32")
                show_error(f"{er1} {stype} {er2}")
                return

        structure_fractions = {
            'a_site': 0,
            'b_site': 0,
            'b_double': 0,
            'spacer': 0,
            'anion': 0
        }

        for element in structure_data:
            try:
                fraction = float(element['fraction'])
            except ValueError:
                show_error(localization_manager.tr("comp_err2"))
                return
            try:
                valence = int(element['valence'])
            except ValueError:
                show_error(localization_manager.tr("comp_err4"))
                return

            stype = element['structure_type']
            structure_fractions[stype] += fraction

        for stype, total in structure_fractions.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                er1 = localization_manager.tr("comp_err31")
                er2 = localization_manager.tr("comp_err32")
                show_error(f"{er1} {stype} {er2}")
                return

        name_phase = self.view.entry_template.get()
        id_template = get_template_id(name_phase)
        id_info = self.model.add_composition_info(id_template, main_data, upd, id_info)

        if not id_info:
            return

        for element in factors_data:
            try:
                k_factor = float(element['k_factor'])
            except ValueError:
                show_error(localization_manager.tr("comp_err5"))
                return
        self.model.add_syntesis_params(id_info, solution_info, upd)

        upd_k = upd
        for factor in factors_data:
            success, message = self.model.add_k_factors(
                id_info,
                factor['salt'],
                factor['k_factor'],
                upd_k
            )
            upd_k = False
            if not success:
                show_error(message)
                return

        upd_sol = upd
        for solvent in solvent_data:
            success, message = self.model.add_solvent(
                id_info,
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
        for element in structure_data:
            success, message = self.model.add_structure(
                id_info,
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
        properties_values = []
        try:
            for property in properties_data:
                properties_values.append(float(property) if property else None)
        except ValueError:
            show_error(localization_manager.tr("comp_err6"))
            return

        success, message = self.model.add_properties(id_info, device_type, properties_values, upd)
        if success:
            show_success(localization_manager.tr("comp_success"))
        else:
            show_error(message)

    def update_composition(self, id_info=None, not_fav=None):
        self.view.update_composition(id_info, not_fav)