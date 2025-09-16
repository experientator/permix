from gui.models.ions_check import IonsCheckModel
from gui.views.ions_check import IonsCheckView

class IonsCheckController:
    def __init__(self, parent):
        self.model = IonsCheckModel()
        self.view = IonsCheckView(parent, self)
        self.load_ions()
        self.view.bind_ion_selection(self.on_ion_selected)
        self.load_ions()

    def handle_submit(self, data):
        success, message = self.model.add_ion(
            data['name'],
            data['ion_type'],
            data['formula'],
            data['valence']
        )
        if success:
            self.view.show_success(message)
        else:
            self.view.show_error("Ошибка", message)

    def ion_handle_submit(self, data):
        if not all(data.values()):
            self.view.show_error("Ошибка","All fields are required")
            return
        try:
            charge = int(data['charge'])
            CN = int(data['CN'])
            ionic_radii = float(data['ionic_radii'])
        except ValueError as e:
            field = str(e).split()[-1]
            self.view.show_error("Ошибка",f"{field} must be a number")
            return

        if not self.model.validate_ion_exists(data['name'], data['ion_type']):
            self.view.show_error("Ошибка","This ion doesn't exist in database")
            return

        if self.model.validate_radii_exists(data['name'], charge, CN):
            self.view.show_error("Ошибка","This ion already exists")
            return

        success, message = self.model.add_ionic_radii(
            data['name'],
            data['ion_type'],
            charge,
            CN,
            ionic_radii
        )

        if success:
            self.view.show_success(message)
        else:
            self.view.show_error("Ошибка",message)

    def load_ions(self):
        try:
            ions = self.model.get_all_ions()
            self.view.show_ions(ions)
        except Exception as e:
            self.view.show_error("Ошибка",f"Не удалось загрузить ионы: {str(e)}")

    def on_ion_selected(self, event=None):
        ion = self.view.get_selected_ion()
        if not ion:
            return
        ion_name, ion_type = ion
        try:
            radii = self.model.get_ionic_radii_for_ion(ion_name, ion_type)
            self.view.show_radii(radii)
        except Exception as e:
            self.view.show_error("Ошибка",f"Не удалось загрузить радиусы: {str(e)}")

    def delete_selected(self):
        item = self.view.get_selected_ion()
        charge, CN, radii = self.view.get_selected_radii()
        if not item:
            self.view.show_warning("Предупреждение", "Выберите строку для удаления")
            return

        record_name = item[0]

        if self.view.ask_confirmation("Подтверждение", "Вы уверены, что хотите удалить эту запись?"):
            try:
                success = self.model.delete_ionic_radii(record_name, charge, CN, radii)
                if success:
                    self.view.show_message("Успех", "Запись успешно удалена")
                    self.load_ions()
                else:
                    self.view.show_error("Ошибка", "Не удалось удалить запись")
            except Exception as e:
                self.view.show_error("Ошибка", f"Ошибка при удалении: {str(e)}")

    def __del__(self):
        self.model.close()