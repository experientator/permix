from gui.models.templates_check import TemplatesCheckModel
from gui.views.templates_check import TemplatesCheckView

class TemplatesCheckController:
    def __init__(self, parent):
        self.model = TemplatesCheckModel()
        self.view = TemplatesCheckView(parent)
        self.load_templates()
        self.view.bind_template_selection(self.on_template_selected)
        self.load_templates()

    def load_templates(self):
        try:
            template = self.model.get_all_templates()
            self.view.show_template(template)
        except Exception as e:
            self.view.show_error("Ошибка", f"Не удалось загрузить ионы: {str(e)}")

    def on_template_selected(self, event=None):
        template = self.view.get_selected_template()
        if not template:
            return

        id_phase, name, anion_stoichiometry, dimensionality, description = template
        try:
            site = self.model.get_sites_for_template(id_phase)
            self.view.show_sites(site)
        except Exception as e:
            self.view.show_error("Ошибка", f"Не удалось загрузить структуру: {str(e)}")

    def __del__(self):
        self.model.close()