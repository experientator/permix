from gui.models.solvents_check import SolventsCheckModel
from gui.views.solvents_check import SolventsCheckView

class SolventsCheckController:
    def __init__(self, parent):
        self.model = SolventsCheckModel()
        self.view = SolventsCheckView(parent, self)
        self.load_data()

    def load_data(self):
        try:
            data = self.model.get_all_solvents()
            self.view.show_data(data)
        except Exception as e:
            self.view.show_error("Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def delete_selected(self):
        item_data = self.view.get_selected_item()
        if not item_data:
            self.view.show_warning("Предупреждение", "Выберите строку для удаления")
            return

        record_id = item_data['values'][0]

        if self.view.ask_confirmation("Подтверждение", "Вы уверены, что хотите удалить эту запись?"):
            try:
                success = self.model.delete_solvent(record_id)
                if success:
                    self.view.show_message("Успех", "Запись успешно удалена")
                    self.load_data()
                else:
                    self.view.show_error("Ошибка", "Не удалось удалить запись")
            except Exception as e:
                self.view.show_error("Ошибка", f"Ошибка при удалении: {str(e)}")

    def __del__(self):
        self.model.close()