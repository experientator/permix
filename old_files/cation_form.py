import tkinter as tk
import sqlite3
import tkinter.messagebox as mb
import tkinter.ttk as ttk

class IonsUploadForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new cation")

        ion_frame = tk.LabelFrame(self)
        ion_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        name = tk.Label(ion_frame, text="name")
        self.entry_name = tk.Entry(ion_frame)
        name.grid(row=0, column=0)
        self.entry_name.grid(row=1, column=0)

        ion_type = ttk.Label(ion_frame, text="type")
        self.box_ion_type = ttk.Combobox(ion_frame, values=["anion", "cation"])
        ion_type.grid(row=0, column=0)
        self.box_ion_type.grid(row=1, column=0)

        formula = tk.Label(ion_frame, text="formula")
        self.entry_formula = tk.Entry(ion_frame)
        formula.grid(row=0, column=1)
        self.entry_formula.grid(row=1, column=1)

        valence = tk.Label(ion_frame, text="valence")
        self.entry_valence = tk.Entry(ion_frame)
        valence.grid(row=0, column=1)
        self.entry_valence.grid(row=1, column=1)

        button = tk.Button(self, text="Enter data", command = self.enter_data)
        button.grid(row = 1, column = 0, sticky="news", padx=20, pady=10)

    def enter_data(self):
        name = self.entry_name.get()
        ion_type = self.box_ion_type.get()
        formula = self.entry_formula.get()
        valence = self.entry_valence.get()

        if not all([name, formula]):
            mb.showerror(title="error", message="All fields are required")
            return

        try:
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Ions 
                                       (id INTEGER PRIMARY KEY, 
                                       name TEXT,
                                       type TEXT,
                                       valence TEXT, 
                                       formula TEXT)
                               '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? OR formula = ? LIMIT 1", (name, formula))
            if cursor.fetchone():
                mb.showerror(title="error", message="Ion with this name or formula already exists")
                return
            else:
                # Insert Data
                data_insert_query = '''INSERT INTO Ions
                                            (name, ion_type, formula, valence) VALUES 
                                            (?, ?, ?, ?)'''
                data_insert_tuple = (name, ion_type, formula, valence)
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()

                mb.showinfo(title="success", message=f"{ion_type} successfully upload")

                self.entry_name.delete(0, tk.END)
                self.entry_formula.delete(0, tk.END)

        except TypeError:
            mb.showerror(title= "error", message="Error: Invalid type operation!")
            return