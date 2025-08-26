from gui.models.templates_check import TemplatesCheckModel
from gui.views.templates_check import TemplatesCheckView

class TemplatesCheckController:
    def __init__(self, parent):
        self.model = TemplatesCheckModel()
        self.view = TemplatesCheckView(parent, self)
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

    def delete_selected(self):
        item_data = self.view.get_selected_template()
        if not item_data:
            self.view.show_warning("Предупреждение", "Выберите строку для удаления")
            return

        record_id = item_data[0]

        if self.view.ask_confirmation("Подтверждение", "Вы уверены, что хотите удалить эту запись?"):
            try:
                success = self.model.delete_template(record_id)
                if success:
                    self.view.show_message("Успех", "Запись успешно удалена")
                    self.load_templates()
                else:
                    self.view.show_error("Ошибка", "Не удалось удалить запись")
            except Exception as e:
                self.view.show_error("Ошибка", f"Ошибка при удалении: {str(e)}")

    def __del__(self):
        self.model.close()

    def __del__(self):
        self.model.close()