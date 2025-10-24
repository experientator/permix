from src.models.candidates_form import CandidateFormModel
from src.views.candidates_form import CandidateFormView
from src.utils.calculation_tests import show_error, show_success

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
            show_success(message)
        else:
            show_error(message)