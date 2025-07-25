import tkinter.messagebox as mb
from gui.models.Ions_form import IonsFormModel
from gui.views.Ions_form import IonsFormView

class IonsFormController:
    def __init__(self, parent):
        self.model = IonsFormModel()
        self.view = IonsFormView(parent, self)

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
            self.view.show_error(message)