import tkinter as tk
import sqlite3
import tkinter.messagebox as mb
import tkinter.ttk as ttk

from Lib.tkinter import IntVar

class Sites(tk.LabelFrame):
    def __init__(self, parent, text):
        super().__init__(parent, text=f"{text}")

        stoich = tk.Label(self, text="base stoichiometry")
        self.entry_stoich = tk.Entry(self)
        stoich.grid(row=0, column=1)
        self.entry_stoich.grid(row=1, column=1)

        valence = tk.Label(self, text="base valence")
        self.entry_valence = tk.Entry(self)
        valence.grid(row=0, column=2)
        self.entry_valence.grid(row=1, column=2)

    def create_site(self):
        pass

class TemplateUploadForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new phase template")

        phase_template = tk.LabelFrame(self)
        phase_template.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        name = tk.Label(phase_template, text="name")
        self.entry_name = tk.Entry(phase_template)
        name.grid(row=0, column=0)
        self.entry_name.grid(row=1, column=0)

        dimensionality = tk.Label(phase_template, text="dimensionality")
        self.entry_dimensionality = tk.Entry(phase_template)
        dimensionality.grid(row=0, column=1)
        self.entry_dimensionality.grid(row=1, column=1)

        description = tk.Label(phase_template, text="description")
        self.entry_description = tk.Entry(phase_template)
        description.grid(row=0, column=1)
        self.entry_description.grid(row=1, column=2)

        anion_stoich = tk.Label(phase_template, text="anion stoichiometry")
        self.entry_anion_stoich = tk.Entry(phase_template)
        anion_stoich.grid(row=0, column=1)
        self.entry_anion_stoich.grid(row=1, column=2)

        label_sites = tk.Label(self, text="choose elements")
        label_sites.grid(row=1, column=0, sticky="news", padx=20, pady=10)

        self.a_site, self.b_site, self.b_double, self.spacer = IntVar()
        self.a_site_checkbutton = ttk.Checkbutton(text="A site", variable=self.a_site)
        self.a_site_checkbutton.grid(row=2, column=0)
        self.b_site_checkbutton = ttk.Checkbutton(text="B site", variable=self.b_site)
        self.b_site_checkbutton.grid(row=2, column=1)
        self.b_double_checkbutton = ttk.Checkbutton(text="B double site", variable=self.b_double)
        self.b_double_checkbutton.grid(row=2, column=2)
        self.spacer_checkbutton = ttk.Checkbutton(text="Spacer", variable=self.spacer)
        self.spacer_checkbutton.grid(row=0, column=3)

        button = tk.Button(self, text="Enter data", command = self.enter_info)
        button.grid(row = 2, column = 0, sticky="news", padx=20, pady=10)

    def enter_info(self):
        if self.a_site:
            a_site_frame = Sites(self, "A site")
            a_site_frame.pack(fill='x', pady=5)
        else:
            pass
        if self.b_site:
            b_site_frame = Sites(self, "B site")
            b_site_frame.pack(fill='x', pady=5)
        else:
            pass
        if self.b_double:
            b_double_frame = Sites(self, "B double")
            b_double_frame.pack(fill='x', pady=5)
        else:
            pass
        if self.spacer:
            spacer_frame = Sites(self, "Spacer")
            spacer_frame.pack(fill='x', pady=5)
        else:
            pass

        # name = self.entry_name.get()
        # ion_type = self.box_ion_type.get()
        # formula = self.entry_formula.get()
        # valence = self.entry_valence.get()
        #
        # if not all([name, formula]):
        #     mb.showerror(title="error", message="All fields are required")
        #     return
        #
        # try:
        #     conn = sqlite3.connect('data.db')
        #     table_create_query = '''CREATE TABLE IF NOT EXISTS Ions
        #                                (id INTEGER PRIMARY KEY,
        #                                name TEXT,
        #                                type TEXT,
        #                                valence TEXT,
        #                                formula TEXT)
        #                        '''
        #     conn.execute(table_create_query)
        #     cursor = conn.cursor()
        #     cursor.execute("SELECT 1 FROM Ions WHERE name = ? OR formula = ? LIMIT 1", (name, formula))
        #     if cursor.fetchone():
        #         mb.showerror(title="error", message="Ion with this name or formula already exists")
        #         return
        #     else:
        #         # Insert Data
        #         data_insert_query = '''INSERT INTO Ions
        #                                     (name, ion_type, formula, valence) VALUES
        #                                     (?, ?, ?, ?)'''
        #         data_insert_tuple = (name, ion_type, formula, valence)
        #         cursor.execute(data_insert_query, data_insert_tuple)
        #         conn.commit()
        #         conn.close()
        #
        #         mb.showinfo(title="success", message=f"{ion_type} successfully upload")
        #
        #         self.entry_name.delete(0, tk.END)
        #         self.entry_formula.delete(0, tk.END)
        #
        # except TypeError:
        #     mb.showerror(title= "error", message="Error: Invalid type operation!")
        #     return