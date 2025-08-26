import tkinter as tk
from gui.default_style import AppStyles

class CandidateFormView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.title("Add new candidates")
        self.attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)

        self.create_widgets()

    def create_widgets(self):
        ion_frame = tk.LabelFrame(self, **AppStyles.frame_style())
        ion_frame.grid(row=0, column=0, sticky="news")

        tk.Label(ion_frame, text="Ключ", **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_name = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0)

        tk.Label(ion_frame, text="Катионы", **AppStyles.label_style()).grid(row=0, column=3)
        self.entry_candidates = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_candidates.grid(row=1, column=3)

        tk.Button(self, text="Enter data",
                  command=self.on_submit, **AppStyles.button_style()).grid(row=1, column=0, sticky="news")

    def on_submit(self):
        data = {
            'name': self.entry_name.get(),
            'candidates': self.entry_candidates.get()
        }
        self.controller.handle_submit(data)

    def show_success(self, message):
        tk.messagebox.showinfo(title="success", message=message)
        self.clear_form()

    def show_error(self, message):
        tk.messagebox.showerror(title="error", message=message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_candidates.delete(0, tk.END)