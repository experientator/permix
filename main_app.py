import tkinter as tk
from tkinter import ttk
from gui.controllers.ions_check import IonsCheckController
from gui.controllers.solvents_check import SolventsCheckController
from gui.controllers.composition_form import CompositionController
from gui.controllers.candidates_form import CandidatesFormController
from gui.controllers.templates_check import TemplatesCheckController
from gui.controllers.user_config_form import UserConfigController
from gui.controllers.composition_check import CompositionCheckController
from gui.views.user_config_form import UserConfigView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PerMix")
        self.wm_attributes('-fullscreen',True)
        menu = tk.Menu(self)
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        upload_menu = tk.Menu(menu, tearoff=0)
        view_menu = tk.Menu(menu, tearoff=0)

        self.calc_controller = UserConfigController(self.main_frame)
        self.calc_view = UserConfigView(self.main_frame, self.calc_controller)
        self.calc_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        upload_menu.add_command(label="Загрузить структуру", command=self.open_comp_form)
        #upload_menu.add_command(label="Загрузить кандидатов", command=self.open_candidate_form)

        view_menu.add_command(label="Просмотр растворителей",  command=self.get_solvents)
        view_menu.add_command(label="Просмотр ионных радиусов",  command=self.get_ionic_radii)
        view_menu.add_command(label="Просмотр шаблонов",  command=self.get_templates)
        view_menu.add_command(label="Просмотр соединений", command=self.get_compositions)

        menu.add_cascade(label="Загрузить", menu=upload_menu)
        menu.add_cascade(label="Просмотреть", menu=view_menu)
        menu.add_command(label="О программе", command= self.program_info)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)

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
        pass

    def open_candidate_form(self):
        CandidatesFormController(self)

    def open_comp_form(self):
        CompositionController(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()