import tkinter as tk
import sqlite3
import tkinter.messagebox as mb

class CationUploadForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new cation")

        cation_frame = tk.LabelFrame(self)
        cation_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        name = tk.Label(cation_frame, text="name")
        self.entry_name = tk.Entry(cation_frame)
        name.grid(row=0, column=0)
        self.entry_name.grid(row=1, column=0)

        formula = tk.Label(cation_frame, text="formula")
        self.entry_formula = tk.Entry(cation_frame)
        formula.grid(row=0, column=1)
        self.entry_formula.grid(row=1, column=1)

        button = tk.Button(self, text="Enter data", command = self.enter_data)
        button.grid(row = 1, column = 0, sticky="news", padx=20, pady=10)

    def enter_data(self):
        name = self.entry_name.get()
        formula = self.entry_formula.get()

        if not all([name, formula]):
            mb.showerror(title="error", message="All fields are required")
            return

        try:
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Cations 
                                       (id INTEGER PRIMARY KEY, 
                                       name TEXT, 
                                       formula TEXT)
                               '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Cations WHERE name = ? OR formula = ? LIMIT 1", (name, formula))
            if cursor.fetchone():
                mb.showerror(title="error", message="Cations with this name or formula already exists")
                return
            else:
                # Insert Data
                data_insert_query = '''INSERT INTO Cations
                                            (name, formula) VALUES 
                                            (?, ?)'''
                data_insert_tuple = (name, formula)
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()

                mb.showinfo(title="success", message="cation successfully upload")

                self.entry_name.delete(0, tk.END)
                self.entry_formula.delete(0, tk.END)

        except TypeError:
            mb.showerror(title= "error", message="Error: Invalid type operation!")
            return