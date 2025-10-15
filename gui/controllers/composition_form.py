from collections import namedtuple

from analysis.database_utils import get_template_id
from gui.models.composition_form import CompositionModel
from gui.views.composition_form import CompositionView
from gui.language.manager import localization_manager

Numbers = namedtuple("Numbers", ["elements", "solvent"])

class CompositionController:
    def __init__(self, parent):
        self.model = CompositionModel()
        self.view = CompositionView(parent, self)
        localization_manager.register_observer(self)

    def handle_main_submit(self, main_data,  solution_info, structure_data,
                           solvent_data, properties_data, factors_data):

        device_type = self.view.entry_device_type.get()

        solvent_fractions = {'solvent': 0, 'antisolvent': 0}
        for solvent in solvent_data:
            try:
                fraction = float(solvent['fraction'])
            except ValueError:
                self.view.show_error(localization_manager.tr("comp_err2"))
                return

            solvent_type = solvent['solvent_type']
            solvent_fractions[solvent_type] += fraction

        for stype, total in solvent_fractions.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                er1 = localization_manager.tr("comp_err31")
                er2 = localization_manager.tr("comp_err32")
                self.view.show_error(f"{er1} {stype} {er2}")
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
                self.view.show_error(localization_manager.tr("comp_err2"))
                return
            try:
                valence = int(element['valence'])
            except ValueError:
                self.view.show_error(localization_manager.tr("comp_err4"))
                return

            stype = element['structure_type']
            structure_fractions[stype] += fraction

        for stype, total in structure_fractions.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                er1 = localization_manager.tr("comp_err31")
                er2 = localization_manager.tr("comp_err32")
                self.view.show_error(f"{er1} {stype} {er2}")
                return

        name_phase = self.view.entry_template.get()
        id_template = get_template_id(name_phase)
        id_info = self.model.add_composition_info(id_template, main_data)

        if not id_info:
            return

        for element in factors_data:
            try:
                k_factor = float(element['k_factor'])
            except ValueError:
                self.view.show_error(localization_manager.tr("comp_err5"))
                return
        self.model.add_syntesis_params(id_info, solution_info)

        for factor in factors_data:
            success, message = self.model.add_k_factors(
                id_info,
                factor['salt'],
                factor['k_factor']
            )
            if not success:
                self.view.show_error(message)
                return

        for solvent in solvent_data:
            success, message = self.model.add_solvent(
                id_info,
                solvent['solvent_type'],
                solvent['symbol'],
                float(solvent['fraction'])
            )
            if not success:
                self.view.show_error(message)
                return

        for element in structure_data:
            success, message = self.model.add_structure(
                id_info,
                element['structure_type'],
                element['symbol'],
                float(element['fraction']),
                int(element['valence'])
            )
            if not success:
                self.view.show_error(message)
                return
        properties_values = []
        try:
            for property in properties_data:
                properties_values.append(float(property) if property else None)
        except ValueError:
            self.view.show_error(localization_manager.tr("comp_err6"))
            return

        success, message = self.model.add_properties(id_info, device_type, properties_values)
        if success:
            self.view.show_success(localization_manager.tr("comp_success"))
        else:
            self.view.show_error(message)