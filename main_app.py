import tkinter as tk
from gui.forma import AddCompositionForm
from gui.solv_form import AddSolventForm
from gui.cation_form import IonsUploadForm
from gui.ionic_radii_form import IonicRadiiUploadForm

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        menu = tk.Menu(self)
        upload_menu = tk.Menu(menu, tearoff=0)
        view_menu = tk.Menu(menu, tearoff=0)

        upload_menu.add_command(label="Загрузить структуру", command=self.open_comp_form)
        upload_menu.add_command(label="Загрузить растворитель", command=self.open_solv_form)
        upload_menu.add_command(label="Загрузить цены на прекурсоры", command=self.open_prices_form)
        upload_menu.add_command(label="Загрузить катионы/анионы", command=self.open_ions_form)
        upload_menu.add_command(label="Загрузить ионные радиусы", command=self.open_ionic_radii_form)

        view_menu.add_command(label="Просмотр структуры")
        view_menu.add_command(label="Просмотр растворителей")
        view_menu.add_command(label="Просмотр цен")

        menu.add_cascade(label="Загрузить", menu=upload_menu)
        menu.add_cascade(label="Просмотреть", menu=view_menu)
        menu.add_command(label="О программе")
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)

    def open_comp_form(self):
        form = AddCompositionForm(self)
        form.grab_set()
        self.wait_window(form)

    def open_solv_form(self):
        form = AddSolventForm(self)
        form.grab_set()
        self.wait_window(form)

    def open_ions_form(self):
        form = IonsUploadForm(self)
        form.grab_set()
        self.wait_window(form)

    def open_prices_form(self):
        form = AddSolventForm(self)
        form.grab_set()
        self.wait_window(form)

    def open_ionic_radii_form(self):
        form = IonicRadiiUploadForm(self)
        form.grab_set()
        self.wait_window(form)

if __name__ == "__main__":
    app = App()
    app.mainloop()