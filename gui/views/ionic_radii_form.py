import tkinter as tk
from tkinter import ttk
from gui.default_style import AppStyles

class IonicRadiiView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Добавить новый ионный радиус")
        self.styles = AppStyles()
        self.build_ui()

    def build_ui(self):
        ion_frame = tk.LabelFrame(self, **AppStyles.frame_style())
        ion_frame.grid(row=0, column=0, sticky="news")

        tk.Label(ion_frame, text="Название", **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_name = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0)
        tk.Label(ion_frame, text="Тип иона", **AppStyles.label_style()).grid(row=0, column=1)
        self.ion_box = ttk.Combobox(ion_frame, values=["cation", "anion"], **AppStyles.combobox_config())
        self.ion_box.grid(row=1, column=1)
        tk.Label(ion_frame, text="Заряд", **AppStyles.label_style()).grid(row=0, column=2)
        self.entry_charge = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_charge.grid(row=1, column=2)
        tk.Label(ion_frame, text="Координационное число", **AppStyles.label_style()).grid(row=0, column=3)
        self.entry_CN = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_CN.grid(row=1, column=3)
        tk.Label(ion_frame, text="Ионный радиус", **AppStyles.label_style()).grid(row=0, column=4)
        self.entry_ionic_radii = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_ionic_radii.grid(row=1, column=4)

        tk.Button(self, text="Добавить ион",
                  command=self.on_submit
                  , **AppStyles.button_style()).grid(row=1, column=0, sticky="news")

    def on_submit(self):
        data = {
            'name': self.entry_name.get(),
            'ion_type': self.ion_box.get(),
            'charge': self.entry_charge.get(),
            'CN': self.entry_CN.get(),
            'ionic_radii': self.entry_ionic_radii.get()
        }
        self.controller.handle_submit(data)

    def show_success(self, message):
        tk.messagebox.showinfo(title="success", message=message)
        self.clear_form()

    def show_error(self, message):
        tk.messagebox.showerror(title="error", message=message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.ion_box.delete(0, tk.END)
        self.entry_charge.delete(0, tk.END)
        self.entry_CN.delete(0, tk.END)
        self.entry_ionic_radii.delete(0, tk.END)