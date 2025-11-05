import tkinter as tk
from tkinter import ttk
from src.controllers.ions_check import IonsCheckController
from src.controllers.solvents_check import SolventsCheckController
from src.controllers.composition_form import CompositionController
from src.controllers.candidates_form import CandidatesFormController
from src.controllers.templates_check import TemplatesCheckController
from src.controllers.user_config_form import UserConfigController
from src.controllers.composition_check import CompositionCheckController
from src.views.user_config_form import UserConfigView
from src.language.manager import localization_manager
from src.language.default_widgets import default_translations
from src.views.about_program_view import AboutProgramView
from src.utils.init_database import init_database

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PerMix")
        try:
            self.state('zoomed')
        except:
            try:
                self.attributes('-zoomed', True)
            except:
                self.geometry("1200x800")
        self.main_frame = None
        self.create_calc()
        self.create_menu()

    def create_calc(self):
        if self.main_frame:
            self.main_frame.destroy()
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.calc_controller = UserConfigController(self.main_frame)
        self.calc_view = UserConfigView(self.main_frame, self.calc_controller)
        self.calc_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_menu(self):
        menu = tk.Menu(self)
        view_menu = tk.Menu(menu, tearoff=0)
        lang_menu = tk.Menu(menu, tearoff=0)

        view_menu.add_command(label=localization_manager.tr("main_2"),
                              command=self.get_solvents)
        view_menu.add_command(label=localization_manager.tr("main_3"),
                              command=self.get_ionic_radii)
        view_menu.add_command(label=localization_manager.tr("main_4"),
                              command=self.get_templates)
        view_menu.add_command(label=localization_manager.tr("main_5"),
                              command=self.get_compositions)

        lang_menu.add_command(label=localization_manager.tr("main_10"),
                              command=self.get_english)
        lang_menu.add_command(label=localization_manager.tr("main_11"),
                              command=self.get_russian)

        menu.add_cascade(label=localization_manager.tr("main_7"),
                         menu=view_menu)
        menu.add_cascade(label=localization_manager.tr("main_12"),
                         menu=lang_menu)

        menu.add_command(label=localization_manager.tr("main_8"),
                         command=self.program_info)
        menu.add_command(label=localization_manager.tr("main_9"),
                         command=self.destroy)

        self.config(menu=menu)

    def get_english(self):
        localization_manager.set_language("en")
        self.create_calc()
        self.create_menu()

    def get_russian(self):
        localization_manager.set_language("ru")
        self.create_calc()
        self.create_menu()

    def get_compositions(self):
        CompositionCheckController(self)

    def get_user_config(self):
        UserConfigController(self)

    def get_templates(self):
        TemplatesCheckController(self)

    def get_ionic_radii(self):
        IonsCheckController(self)

    def get_solvents(self):
        SolventsCheckController(self)

    def program_info(self):
        AboutProgramView(self)

    def open_candidate_form(self):
        CandidatesFormController(self)

    def open_comp_form(self):
        CompositionController(self)

    def return_from_composition_check(self, id_info=None, not_fav=None):
        self.calc_view.return_from_composition_check(id_info, not_fav)

localization_manager.initialize_default_translations(default_translations)

if __name__ == "__main__":
    init_database()
    app = App()
    app.mainloop()