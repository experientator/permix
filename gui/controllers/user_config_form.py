from gui.views.user_config_form import UserConfigView

class UserConfigController:
    def __init__(self, parent):
        self.view = UserConfigView(parent, self)