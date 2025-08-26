import tkinter as tk
import tkinter.ttk as ttk
from gui.default_style import AppStyles

class IonsFormView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Добавить новый ион")
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)
        self.create_widgets()

    def create_widgets(self):
        ion_frame = tk.LabelFrame(self, **AppStyles.frame_style())
        ion_frame.grid(row=0, column=0)

        tk.Label(ion_frame, text="Название",
                 **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_name = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0)

        tk.Label(ion_frame, text="Тип иона",
                 **AppStyles.label_style()).grid(row=0, column=1)
        self.box_ion_type = ttk.Combobox(ion_frame,
                                         values=["анион", "катион"],
                                         **AppStyles.combobox_config())
        self.box_ion_type.current(0)
        self.box_ion_type.grid(row=1, column=1)

        tk.Label(ion_frame, text="Формула",
                 **AppStyles.label_style()).grid(row=0, column=2)
        self.entry_formula = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_formula.grid(row=1, column=2)

        tk.Label(ion_frame, text="Валентность",
                 ** AppStyles.label_style()
                 ).grid(row=0, column=3)
        self.entry_valence = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_valence.grid(row=1, column=3)

        tk.Button(self, text="Добавить ион",
                  **AppStyles.button_style(),
                  command=self.on_submit).grid(row=1, column=0)

    def on_submit(self):
        type = ""

        if self.box_ion_type.get() == "анион":
            type = "anion"
        if self.box_ion_type.get() == "катион":
            type = "cation"

        data = {
            'name': self.entry_name.get(),
            'ion_type': type,
            'formula': self.entry_formula.get(),
            'valence': self.entry_valence.get()
        }
        self.controller.handle_submit(data)

    def show_success(self, message):
        tk.messagebox.showinfo(title="success", message=message)
        self.clear_form()

    def show_error(self, message):
        tk.messagebox.showerror(title="error", message=message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_formula.delete(0, tk.END)
        self.entry_valence.delete(0, tk.END)