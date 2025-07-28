from gui.models.ionic_radii_form import IonicRadiiModel
from gui.views.ionic_radii_form import IonicRadiiView

class IonicRadiiController:
    def __init__(self, parent):
        self.model = IonicRadiiModel()
        self.view = IonicRadiiView(parent, self)

    def handle_submit(self, data):

        if not all(data.values()):
            self.view.show_error("All fields are required")
            return
        try:
            charge = int(data['charge'])
            CN = int(data['CN'])
            ionic_radii = float(data['ionic_radii'])
        except ValueError as e:
            field = str(e).split()[-1]
            self.view.show_error(f"{field} must be a number")
            return

        if not self.model.validate_ion_exists(data['name'], data['ion_type']):
            self.view.show_error("This ion doesn't exist in database")
            return

        if self.model.validate_radii_exists(data['name'], charge, CN):
            self.view.show_error("This ion already exists")
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
            self.view.show_error(message)