import tkinter as tk

class CandidateFormView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Add new candidates")

        self.create_widgets()

    def create_widgets(self):
        ion_frame = tk.LabelFrame(self)
        ion_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        tk.Label(ion_frame, text="name").grid(row=0, column=0)
        self.entry_name = tk.Entry(ion_frame)
        self.entry_name.grid(row=1, column=0)

        tk.Label(ion_frame, text="cations").grid(row=0, column=3)
        self.entry_candidates = tk.Entry(ion_frame)
        self.entry_candidates.grid(row=1, column=3)

        tk.Button(self, text="Enter data",
                  command=self.on_submit).grid(row=1, column=0, sticky="news", padx=20, pady=10)

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