from collections import namedtuple

from analysis.database_utils import get_template_id
from gui.models.composition_form import CompositionModel
from gui.views.composition_form import CompositionView

Numbers = namedtuple("Numbers", ["elements", "solvent"])


class CompositionController:
    def __init__(self, parent):
        self.model = CompositionModel()
        self.view = CompositionView(parent, self)

    def handle_info_submit(self, data):
        try:
            num_elements = int(data['num_elements'])
            num_solvents = int(data['num_solvents'])
            num_k = int(data['num_k'])
        except ValueError:
            self.view.show_error("Number of elements, solvents and k_factors must be float numbers")
            return

        id_info = self.model.add_composition_info(
            data['id_template'],
            data['doi'],
            data['data_type'],
            data['notes']
        )

        if id_info:
            self.view.create_dynamic_widgets(num_elements, num_solvents, num_k)
            self.view.first_button.destroy()
            return id_info
        return None

    def handle_main_submit(self, structure_data, solvent_data, properties_data, factors_data):
        solvent_fractions = {'solvent': 0, 'antisolvent': 0}
        for solvent in solvent_data:
            try:
                fraction = float(solvent['fraction'])
            except ValueError:
                self.view.show_error("Fraction must be a float number")
                return

            solvent_type = solvent['solvent_type']
            solvent_fractions[solvent_type] += fraction

        for stype, total in solvent_fractions.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                self.view.show_error(f"Total fraction for {stype} must be 1")
                return

        structure_fractions = {
            'A_site': 0,
            'B_site': 0,
            'B_double': 0,
            'spacer_site': 0,
            'anion': 0
        }

        for element in structure_data:
            try:
                fraction = float(element['fraction'])
                valence = int(element['valence'])
            except ValueError:
                self.view.show_error("Fraction must be float and valence must be integer")
                return

            stype = element['structure_type']
            structure_fractions[stype] += fraction

        for stype, total in structure_fractions.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                self.view.show_error(f"Total fraction for {stype} must be 1")
                return

        name_phase = self.view.phase_template.get()
        id_template = get_template_id(name_phase)
        id_info = self.handle_info_submit({
            'doi': self.view.entry_doi.get(),
            'data_type': self.view.data_box.get(),
            'notes': self.view.entry_notes.get(),
            'id_template': id_template,
            'num_elements': len(structure_data),
            'num_solvents': len(solvent_data),
            'num_k': len(factors_data)
        })

        if not id_info:
            return

        for element in factors_data:
            try:
                k_factor = float(element['k_factor'])
            except ValueError:
                self.view.show_error("k factors must be float number")
                return

        for factor in factors_data:
            success, message = self.model.add_k_factors(
                id_info,
                factor['precursor'],
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

        try:
            properties_values = [
                float(properties_data['band_gap']) if properties_data['band_gap'] else None,
                float(properties_data['ff_percent']) if properties_data['ff_percent'] else None,
                float(properties_data['pce_percent']) if properties_data['pce_percent'] else None,
                float(properties_data['voc']) if properties_data['voc'] else None,
                float(properties_data['jsc']) if properties_data['jsc'] else None,
                properties_data['stability_notes'],
                float(properties_data['v_antisolvent']) if properties_data['v_antisolvent'] else None,
                float(properties_data['v_solution']) if properties_data['v_solution'] else None,
                float(properties_data['c_solution']) if properties_data['c_solution'] else None,
                float(properties_data['anion_stoichiometry']) if properties_data['anion_stoichiometry'] else None,
                properties_data['method_description'] if properties_data['method_description'] else None
            ]
        except ValueError:
            self.view.show_error("All numeric properties must be valid numbers")
            return

        success, message = self.model.add_properties(id_info, properties_values)
        if success:
            self.view.show_success("Composition successfully added to database")
        else:
            self.view.show_error(message)