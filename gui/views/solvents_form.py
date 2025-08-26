import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
from gui.default_style import AppStyles

class SolventFormView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Добавить новый растворитель")
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)
        self.styles = AppStyles()
        self.build_ui()

    def build_ui(self):

        solv_frame = tk.LabelFrame(self, **AppStyles.frame_style())
        solv_frame.grid(row=0, column=0, sticky="news")
        tk.Label(solv_frame, text="Название",
                 **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_name = tk.Entry(solv_frame,
                 **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0)
        tk.Label(solv_frame, text="Тип",
                 **AppStyles.label_style()).grid(row=0, column=1)
        self.box_solvent_type = ttk.Combobox(solv_frame,
                                             values=["Растворитель", "Антирастворитель"],
                                             **AppStyles.combobox_config())
        self.box_solvent_type.grid(row=1, column=1)
        self.box_solvent_type.current(0)
        tk.Label(solv_frame, text="Формула",
                 **AppStyles.label_style()).grid(row=0, column=2)
        self.entry_formula = tk.Entry(solv_frame,
                 **AppStyles.entry_style())
        self.entry_formula.grid(row=1, column=2)
        tk.Label(solv_frame, text="Плотность, г/мл",
                 **AppStyles.label_style()).grid(row=0, column=3)
        self.entry_density = tk.Entry(solv_frame,
                 **AppStyles.entry_style())
        self.entry_density.grid(row=1, column=3)
        tk.Label(solv_frame, text="Температура кипения, C",
                 **AppStyles.label_style()).grid(row=0, column=4)
        self.entry_bp = tk.Entry(solv_frame,
                 **AppStyles.entry_style())
        self.entry_bp.grid(row=1, column=4)
        tk.Label(solv_frame, text="Заметки",
                 **AppStyles.label_style()).grid(row=0, column=5)
        self.entry_notes = tk.Entry(solv_frame,
                 **AppStyles.entry_style())
        self.entry_notes.grid(row=1, column=5)

        tk.Button(self, text="Загрузить данные",
                  command=self.on_submit,
                 **AppStyles.button_style()).grid(row=1, column=0)

    def on_submit(self):
        type = ""
        if self.box_solvent_type.get() == "Растворитель":
            type = "solvent"
        if self.box_solvent_type.get() == "Антирастворитель":
            type = "antisolvent"
        data = {
            'name': self.entry_name.get(),
            'type': type,
            'formula': self.entry_formula.get(),
            'density': self.entry_density.get(),
            'boiling_point': self.entry_bp.get(),
            'notes': self.entry_notes.get()
        }
        self.controller.handle_submit(data)

    def show_success(self, message):
        mb.showinfo(title="success", message=message)
        self.clear_form()

    def show_error(self, message):
        mb.showerror(title="error", message=message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.box_solvent_type.set('')
        self.entry_formula.delete(0, tk.END)
        self.entry_density.delete(0, tk.END)
        self.entry_bp.delete(0, tk.END)
        self.entry_notes.delete(0, tk.END)