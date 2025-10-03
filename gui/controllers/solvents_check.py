from gui.models.solvents_check import SolventsCheckModel
from gui.views.solvents_check import SolventsCheckView
from gui.language.manager import localization_manager

class SolventsCheckController:
    def __init__(self, parent):
        self.model = SolventsCheckModel()
        self.view = SolventsCheckView(parent, self)
        localization_manager.register_observer(self)
        self.load_data()

    def load_data(self):
        try:
            data = self.model.get_all_solvents()
            self.view.show_data(data)
        except Exception as e:
            self.view.show_error(localization_manager.tr("sol_err1"))

    def delete_selected(self):
        item_data = self.view.get_selected_item()
        if not item_data:
            self.view.show_warning(localization_manager.tr("ion_war"))
            return

        record_id = item_data['values'][0]

        if self.view.ask_confirmation(localization_manager.tr("ion_conf")):
            try:
                success = self.model.delete_solvent(record_id)
                if success:
                    self.view.show_success(localization_manager.tr("ion_success"))
                    self.load_data()
                else:
                    self.view.show_error(localization_manager.tr("ion_err7"))
            except Exception as e:
                er = localization_manager.tr("ion_err8")
                self.view.show_error(f"{er} {str(e)}")

    def handle_submit(self, data):

        if not all([data['name'], data['type'], data['formula'], data['density'], data['boiling_point']]):
            self.view.show_error(localization_manager.tr("sol_err2"))
            return
        try:
            density = float(data['density'])
            boiling_point = float(data['boiling_point'])
        except ValueError:
            self.view.show_error(localization_manager.tr("sol_err3"))
            return

        success, message = self.model.add_solvent(
            data['name'],
            data['type'],
            data['formula'],
            density,
            boiling_point,
            data['notes']
        )

        if success:
            self.view.show_success(message)
            self.load_data()
        else:
            self.view.show_error(message)

    def __del__(self):
        self.model.close()