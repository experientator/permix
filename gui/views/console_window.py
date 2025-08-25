import tkinter as tk
from tkinter import ttk, scrolledtext

class ConsoleWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.console_text = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="black",
            fg="white",
            insertbackground="white"
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.console_text.config(state=tk.DISABLED)

        clear_btn = ttk.Button(self, text="Очистить", command=self.clear_console)
        clear_btn.pack(pady=5)

    def add_text(self, text):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, text)
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)

    def clear_console(self):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)