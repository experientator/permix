import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import tkinter.messagebox as mb

class IonicRadiiUploadForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new ionic radii")

        ion_frame = tk.LabelFrame(self)
        ion_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        name = tk.Label(ion_frame, text="name")
        self.entry_name = tk.Entry(ion_frame)
        name.grid(row=0, column=0)
        self.entry_name.grid(row=1, column=0)

        ion_type = tk.Label(ion_frame, text="ion type")
        self.ion_box = ttk.Combobox(ion_frame, values=["cation", "anion"])
        ion_type.grid(row=0, column=1)
        self.ion_box.grid(row=1, column=1)

        charge = tk.Label(ion_frame, text="charge")
        self.entry_charge = tk.Entry(ion_frame)
        charge.grid(row=0, column=2)
        self.entry_charge.grid(row=1, column=2)

        CN = tk.Label(ion_frame, text="coordinate number")
        self.entry_CN = tk.Entry(ion_frame)
        CN.grid(row=0, column=3)
        self.entry_CN.grid(row=1, column=3)

        ionic_radii = tk.Label(ion_frame, text="ionic radii")
        self.entry_ionic_radii = tk.Entry(ion_frame)
        ionic_radii.grid(row=0, column=4)
        self.entry_ionic_radii.grid(row=1, column=4)

        button = tk.Button(self, text="Enter data", command = self.enter_data)
        button.grid(row = 1, column = 0, sticky="news", padx=20, pady=10)

    def enter_data(self):
        name = self.entry_name.get()
        ion_type = self.ion_box.get()
        charge = self.entry_charge.get()
        CN = self.entry_CN.get()
        ionic_radii = self.entry_ionic_radii.get()

        if not all([name, ion_type, charge, CN, ionic_radii]):
            mb.showerror(title="error", message="All fields are required")
            return

        try:
            charge = int(charge)
        except ValueError:
            mb.showerror(title="error", message="charge must be integer number")
            return

        try:
            CN = int(CN)
        except ValueError:
            mb.showerror(title="error", message="coordinate number must be integer number")
            return

        try:
            ionic_radii = float(ionic_radii)
        except ValueError:
            mb.showerror(title="error", message="ionic radii must be float number")
            return

        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? AND ion_type = ?", (name, ion_type))
            if cursor.fetchone():
                cursor.close()
                table_create_query = '''CREATE TABLE IF NOT EXISTS Ionic_radii 
                                                       (id INTEGER PRIMARY KEY,
                                                       name TEXT,
                                                       ion_type TEXT,
                                                       charge INT, 
                                                       CN INT,
                                                       ionic_radii FLOAT,
                                                       FOREIGN KEY (name) REFERENCES Ions (name))
                                               '''
                conn.execute(table_create_query)
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM Ionic_radii WHERE name = ? AND charge = ? AND CN = ?"
                               , (name, charge, CN))
                if cursor.fetchone():
                    mb.showerror(title="error", message="this ion already exists")
                    return
                else:
                    # Insert Data
                    data_insert_query = '''INSERT INTO Ionic_radii
                                                            (name, ion_type, charge, CN, ionic_radii) VALUES 
                                                            (?, ?, ?, ?, ?)'''
                    data_insert_tuple = (name, ion_type, charge, CN, ionic_radii)
                    cursor.execute(data_insert_query, data_insert_tuple)
                    conn.commit()
                    conn.close()

                    mb.showinfo(title="success", message="ion successfully upload")

                    self.entry_name.delete(0, tk.END)
                    self.ion_box.delete(0, tk.END)
                    self.entry_charge.delete(0, tk.END)
                    self.entry_CN.delete(0, tk.END)
                    self.entry_ionic_radii.delete(0, tk.END)
            else:
                mb.showerror(title="error", message="this ion doesn't exist in database")
                return
        except TypeError:
            mb.showerror(title= "error", message="Error: Invalid type operation!")
            return