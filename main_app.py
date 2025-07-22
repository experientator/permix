import tkinter as tk
from gui.forma import AddCompositionForm
from gui.solv_form import AddSolventForm

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=0)

        file_menu.add_command(label="Загрузить структуру", command=self.open_comp_form)
        file_menu.add_command(label="Просмотр структуры")
        file_menu.add_command(label="Загрузить растворитель", command=self.open_solv_form)
        file_menu.add_command(label="Просмотр растворителей")
        file_menu.add_command(label="Загрузить цены на прекурсоры", command=self.open_prices_form)
        file_menu.add_command(label="Просмотр цен")

        menu.add_cascade(label="Загрузить", menu=file_menu)
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

    def open_prices_form(self):
        form = AddSolventForm(self)
        form.grab_set()
        self.wait_window(form)

if __name__ == "__main__":
    app = App()
    app.mainloop()