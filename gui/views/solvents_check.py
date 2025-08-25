import tkinter as tk
from tkinter import ttk, messagebox
from gui.default_style import AppStyles

class SolventsCheckView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.title("Solvents viewer")

        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self, **AppStyles.frame_style())
        button_frame.pack(pady=10)

        delete_btn = tk.Button(button_frame, text="Удалить выбранное",
                               command=self.controller.delete_selected,
                               **AppStyles.button_style())
        delete_btn.grid(row=0, column=1, padx=5)

        self.tree = ttk.Treeview(self, columns=('name', 'type', 'formula', 'density', 'boiling_point', 'notes'), show='headings')

        self.tree.heading('name', text='название')
        self.tree.heading('type', text='тип')
        self.tree.heading('formula', text='формула')
        self.tree.heading('density', text='плотность')
        self.tree.heading('boiling_point', text='температура кипения')
        self.tree.heading('notes', text='заметки')

        self.tree.column('name', width=150, anchor='center')
        self.tree.column('formula', width=50)
        self.tree.column('type', width=50)
        self.tree.column('density', width=50)
        self.tree.column('boiling_point', width=50)
        self.tree.column('notes', width=150, anchor='center')

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_data(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in data:
            self.tree.insert('', 'end', values=row)

    def get_selected_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        return self.tree.item(selected_item)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def ask_confirmation(self, title, message):
        return messagebox.askyesno(title, message)