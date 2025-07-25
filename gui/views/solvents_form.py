import tkinter as tk
import tkinter.messagebox as mb

class SolventFormView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Add new solvent")
        self.build_ui()

    def build_ui(self):

        solv_frame = tk.LabelFrame(self)
        solv_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)
        tk.Label(solv_frame, text="name").grid(row=0, column=0)
        self.entry_name = tk.Entry(solv_frame)
        self.entry_name.grid(row=1, column=0)
        tk.Label(solv_frame, text="formula").grid(row=0, column=1)
        self.entry_formula = tk.Entry(solv_frame)
        self.entry_formula.grid(row=1, column=1)
        tk.Label(solv_frame, text="density, g/ml").grid(row=0, column=2)
        self.entry_density = tk.Entry(solv_frame)
        self.entry_density.grid(row=1, column=2)
        tk.Label(solv_frame, text="boiling point, C").grid(row=0, column=3)
        self.entry_bp = tk.Entry(solv_frame)
        self.entry_bp.grid(row=1, column=3)
        tk.Label(solv_frame, text="notes").grid(row=0, column=4)
        self.entry_notes = tk.Entry(solv_frame)
        self.entry_notes.grid(row=1, column=4)

        tk.Button(self, text="Enter data",
                  command=self.on_submit).grid(row=1, column=0, sticky="news", padx=20, pady=10)

    def on_submit(self):
        data = {
            'name': self.entry_name.get(),
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
        self.entry_formula.delete(0, tk.END)
        self.entry_density.delete(0, tk.END)
        self.entry_bp.delete(0, tk.END)
        self.entry_notes.delete(0, tk.END)