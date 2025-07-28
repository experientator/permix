from gui.models.ions_check import IonsCheckModel
from gui.views.ions_check import IonsCheckView

class IonsCheckController:
    def __init__(self, parent):
        self.model = IonsCheckModel()
        self.view = IonsCheckView(parent)
        self.load_ions()
        self.view.bind_ion_selection(self.on_ion_selected)
        self.load_ions()

    def load_ions(self):
        try:
            ions = self.model.get_all_ions()
            self.view.show_ions(ions)
        except Exception as e:
            self.view.show_error("Ошибка", f"Не удалось загрузить ионы: {str(e)}")

    def on_ion_selected(self, event=None):
        ion = self.view.get_selected_ion()
        if not ion:
            return

        ion_name, ion_type = ion
        try:
            radii = self.model.get_ionic_radii_for_ion(ion_name, ion_type)
            self.view.show_radii(radii)
        except Exception as e:
            self.view.show_error("Ошибка", f"Не удалось загрузить радиусы: {str(e)}")

    def __del__(self):
        self.model.close()