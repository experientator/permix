import tkinter.messagebox as mb
from gui.views.phase_template_form import TemplateView
from gui.models.phase_template_form import TemplateModel

class TemplateController:
    def __init__(self, parent):
        self.model = TemplateModel()
        self.view = TemplateView(parent, self)
        self.current_template_id = None

    def handle_add_sites(self, data):
        if not all([data['name'], data['dimensionality'], data['anion_stoich']]):
            self.view.show_error("Name, dimensionality and anion stoichiometry are required")
            return

        try:
            dimensionality = int(data['dimensionality'])
            anion_stoich = int(data['anion_stoich'])
        except ValueError:
            self.view.show_error("Dimensionality and anion stoichiometry must be integers")
            return

        template_id, message = self.model.add_template(
            data['name'],
            data['description'],
            anion_stoich,
            dimensionality
        )

        if not template_id:
            self.view.show_error(message)
            return

        self.current_template_id = template_id
        self.view.create_site_frames()

    def handle_submit_template(self, site_data):
        if not self.current_template_id:
            self.view.show_error("No template selected")
            return

        for site in site_data:
            try:
                stoichiometry = int(site['stoichiometry'])
                valence = int(site['valence'])
            except ValueError:
                self.view.show_error("Stoichiometry and valence must be integers")
                return

        for site in site_data:
            success, message = self.model.add_site(
                self.current_template_id,
                int(site['stoichiometry']),
                site['type'],
                site['valence']
            )

            if not success:
                self.view.show_error(message)
                return

        self.view.show_success("Template with sites successfully uploaded")
        self.current_template_id = None