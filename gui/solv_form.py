import tkinter as tk
import sqlite3
import tkinter.messagebox as mb

class AddSolventForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new solvent")

        solv_frame = tk.LabelFrame(self)
        solv_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        name = tk.Label(solv_frame, text="name")
        self.entry_name = tk.Entry(solv_frame)
        name.grid(row=0, column=0)
        self.entry_name.grid(row=1, column=0)

        formula = tk.Label(solv_frame, text="formula")
        self.entry_formula = tk.Entry(solv_frame)
        formula.grid(row=0, column=1)
        self.entry_formula.grid(row=1, column=1)

        density = tk.Label(solv_frame, text="density, g/ml")
        self.entry_density = tk.Entry(solv_frame)
        density.grid(row=0, column=2)
        self.entry_density.grid(row=1, column=2)

        bp = tk.Label(solv_frame, text="boiling point, C")
        self.entry_bp = tk.Entry(solv_frame)
        bp.grid(row=0, column=3)
        self.entry_bp.grid(row=1, column=3)

        notes = tk.Label(solv_frame, text="notes")
        self.entry_notes = tk.Entry(solv_frame)
        notes.grid(row=2, column=1)
        self.entry_notes.grid(row=3, column=1)

        button = tk.Button(self, text="Enter data", command = self.enter_data)
        button.grid(row = 1, column = 0, sticky="news", padx=20, pady=10)

    def enter_data(self):
        name = self.entry_name.get()
        formula = self.entry_formula.get()
        density = self.entry_density.get()
        boiling_point = self.entry_bp.get()
        notes = self.entry_notes.get()

        if not all([name, formula, density, boiling_point]):
            mb.showerror(title="error", message="All fields except notes are required")
            return

        try:
            density = float(density)
            boiling_point = float(boiling_point)
        except ValueError:
            mb.showerror(title="error", message="Density and boiling point must be integer or float numbers")
            return

        try:
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Solvents 
                                       (id INTEGER PRIMARY KEY, 
                                       name TEXT, 
                                       formula TEXT, 
                                       density FLOAT, 
                                       boiling_point FLOAT, 
                                       notes TEXT)
                               '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Solvents WHERE name = ? OR formula = ? LIMIT 1", (name, formula))
            if cursor.fetchone():
                mb.showerror(title="error", message="Solvent with this name or formula already exists")
                return
            else:
                # Insert Data
                data_insert_query = '''INSERT INTO Solvents 
                                            (name, formula, density, boiling_point, notes) VALUES 
                                            (?, ?, ?, ?, ?)'''
                data_insert_tuple = (name, formula, density,
                                     boiling_point, notes)
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()

                mb.showinfo(title="success", message="Solvent successfully upload")

                self.entry_name.delete(0, tk.END)
                self.entry_formula.delete(0, tk.END)
                self.entry_density.delete(0, tk.END)
                self.entry_bp.delete(0, tk.END)
                self.entry_notes.delete(0, tk.END)

        except TypeError:
            mb.showerror(title= "error", message="Error: Invalid type operation!")
            return