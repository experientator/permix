from src.models.ions_check import IonsCheckModel
from src.views.ions_check import IonsCheckView
from src.language.manager import localization_manager
from src.utils.calculation_tests import show_error, show_success, ask_confirmation, show_warning

class IonsCheckController:
    def __init__(self, parent):
        self.model = IonsCheckModel()
        self.view = IonsCheckView(parent, self)
        localization_manager.register_observer(self)

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
            show_success(message)
        else:
            show_error(message)

    def ion_handle_submit(self, data):
        if not all(data.values()):
            show_error(localization_manager.tr("ion_err1"))
            return
        try:
            charge = int(data['charge'])
            CN = int(data['CN'])
            ionic_radii = float(data['ionic_radii'])
        except ValueError as e:
            field = str(e).split()[-1]
            er= localization_manager.tr("ion_err2")
            show_error(f"{field} {er}")
            return

        if not self.model.validate_ion_exists(data['name'], data['ion_type']):
            show_error(localization_manager.tr("ion_err3"))
            return

        if self.model.validate_radii_exists(data['name'], charge, CN):
            show_error(localization_manager.tr("ion_err4"))
            return

        success, message = self.model.add_ionic_radii(
            data['name'],
            data['ion_type'],
            charge,
            CN,
            ionic_radii
        )

        if success:
            show_success(message)
        else:
            show_error(message)

    def load_ions(self):
        try:
            ions = self.model.get_all_ions()
            self.view.show_ions(ions)
        except Exception as e:
            er = localization_manager.tr("ion_err5")
            show_error(f"{er} {str(e)}")

    def on_ion_selected(self, event=None):
        ion = self.view.get_selected_ion()
        if not ion:
            return
        ion_name, ion_type = ion
        try:
            radii = self.model.get_ionic_radii_for_ion(ion_name, ion_type)
            self.view.show_radii(radii)
        except Exception as e:
            er = localization_manager.tr("ion_err6")
            show_error(f"{er} {str(e)}")

    def delete_selected(self):
        item = self.view.get_selected_ion()
        charge, CN, radii = self.view.get_selected_radii()
        if not item:
            show_warning(localization_manager.tr("ion_war"))
            return

        record_name = item[0]

        if ask_confirmation(localization_manager.tr("ion_conf")):
            try:
                success = self.model.delete_ionic_radii(record_name, charge, CN, radii)
                if success:
                    show_success(localization_manager.tr("ion_success"))
                    self.load_ions()
                else:
                    show_error(localization_manager.tr("ion_err7"))
            except Exception as e:
                er = localization_manager.tr("ion_err8")
                show_error(f"{er} {str(e)}")

    def __del__(self):
        self.model.close()