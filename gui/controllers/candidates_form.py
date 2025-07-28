import tkinter.messagebox as mb
from gui.models.candidates_form import CandidateFormModel
from gui.views.candidates_form import CandidateFormView

class CandidatesFormController:
    def __init__(self, parent):
        self.model = CandidateFormModel()
        self.view = CandidateFormView(parent, self)

    def handle_submit(self, data):
        success, message = self.model.add_candidate(
            data['name'],
            data['candidates']
        )
        if success:
            self.view.show_success(message)
        else:
            self.view.show_error(message)