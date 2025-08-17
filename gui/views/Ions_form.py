import tkinter as tk
import tkinter.ttk as ttk
from gui.default_style import AppStyles

class IonsFormView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Add new ion")
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.create_widgets()

    def create_widgets(self):
        ion_frame = tk.LabelFrame(self, **AppStyles.frame_style())
        ion_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        tk.Label(ion_frame, text="name",
                 **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_name = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0)

        tk.Label(ion_frame, text="type",
                 **AppStyles.label_style()).grid(row=0, column=1)
        self.box_ion_type = ttk.Combobox(ion_frame,
                                        ** AppStyles.combobox_style(),
                                         values=["anion", "cation"])
        self.box_ion_type.grid(row=1, column=1)

        tk.Label(ion_frame, text="formula",
                 **AppStyles.label_style()).grid(row=0, column=2)
        self.entry_formula = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_formula.grid(row=1, column=2)

        tk.Label(ion_frame, text="valence",
                 ** AppStyles.label_style()
                 ).grid(row=0, column=3)
        self.entry_valence = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_valence.grid(row=1, column=3)

        tk.Button(self, text="Enter data",
                  **AppStyles.button_style(),
                  command=self.on_submit).grid(row=1, column=0, sticky="news", padx=20, pady=10)

    def on_submit(self):
        data = {
            'name': self.entry_name.get(),
            'ion_type': self.box_ion_type.get(),
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