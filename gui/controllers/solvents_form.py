from gui.models.solvents_form import SolventFormModel
from gui.views.solvents_form import SolventFormView

class SolventController:
    def __init__(self, parent):
        self.model = SolventFormModel()
        self.view = SolventFormView(parent, self)

    def handle_submit(self, data):

        if not all([data['name'], data['formula'], data['density'], data['boiling_point']]):
            self.view.show_error("All fields except notes are required")
            return
        try:
            density = float(data['density'])
            boiling_point = float(data['boiling_point'])
        except ValueError:
            self.view.show_error("Density and boiling point must be numbers")
            return

        success, message = self.model.add_solvent(
            data['name'],
            data['formula'],
            density,
            boiling_point,
            data['notes']
        )

        if success:
            self.view.show_success(message)
        else:
            self.view.show_error(message)