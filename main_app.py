import tkinter as tk
from gui.controllers.Ions_form import IonsFormController
from gui.controllers.solvents_form import SolventController
from gui.controllers.ionic_radii_form import IonicRadiiController
from gui.controllers.composition_form import CompositionController
from gui.controllers.phase_template_form import TemplateController
from gui.controllers.candidates_form import CandidatesFormController

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        menu = tk.Menu(self)
        upload_menu = tk.Menu(menu, tearoff=0)
        view_menu = tk.Menu(menu, tearoff=0)

        upload_menu.add_command(label="Загрузить структуру", command=self.open_comp_form)
        upload_menu.add_command(label="Загрузить растворитель", command=self.open_solv_form)
        upload_menu.add_command(label="Загрузить ионные радиусы", command=self.open_ionic_radii_form)
        upload_menu.add_command(label="Загрузить доступные ионы", command=self.open_ions_form)
        upload_menu.add_command(label="Загрузить шаблон", command=self.open_template_form)
        upload_menu.add_command(label="Загрузить кандидатов", command=self.open_candidate_form)

        view_menu.add_command(label="Просмотр структуры")
        view_menu.add_command(label="Просмотр растворителей")
        view_menu.add_command(label="Просмотр цен")

        menu.add_cascade(label="Загрузить", menu=upload_menu)
        menu.add_cascade(label="Просмотреть", menu=view_menu)
        menu.add_command(label="О программе", command= self.program_info)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)

    def program_info(self):
        pass

    def open_template_form(self):
        TemplateController(self)

    def open_candidate_form(self):
        CandidatesFormController(self)

    def open_comp_form(self):
        CompositionController(self)

    def open_solv_form(self):
        SolventController(self)

    def open_ions_form(self):
        IonsFormController(self)

    def open_prices_form(self):
        pass

    def open_ionic_radii_form(self):
        IonicRadiiController(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()