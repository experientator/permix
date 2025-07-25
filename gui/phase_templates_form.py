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

    def get_data(self):
        stoich = self.entry_stoich.get()
        valence = self.entry_valence.get()
        if not all([stoich, valence]):
            mb.showerror(title="error", message="All fields are required")
            return
        return stoich, valence

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

        #выбор элементов для дальнейшего добавления виджетов
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

        self.element_frames = []
        self.text = ""

    def return_id(self):
        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.execute("SELECT id FROM Phase_templates ORDER BY id DESC LIMIT 1")
            id_template = cursor.fetchone()
        finally:
            conn.close()
        return id_template[0]

    def enter_info(self):
        if self.a_site:
            self.text = "a_site"
            a_site_frame = Sites(self, "A site")
            a_site_frame.pack(fill='x', pady=5)
            self.element_frames.append(a_site_frame)
        else:
            pass
        if self.b_site:
            self.text = "b_site"
            b_site_frame = Sites(self, "B site")
            b_site_frame.pack(fill='x', pady=5)
            self.element_frames.append(b_site_frame)
        else:
            pass
        if self.b_double:
            self.text = "b_double"
            b_double_frame = Sites(self, "B double")
            b_double_frame.pack(fill='x', pady=5)
            self.element_frames.append(b_double_frame)
        else:
            pass
        if self.spacer:
            self.text = "spacer"
            spacer_frame = Sites(self, "Spacer")
            spacer_frame.pack(fill='x', pady=5)
            self.element_frames.append(spacer_frame)
        else:
            pass

        button = tk.Button(self, text="Enter elements", command=self.enter_elements)
        button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

        name = self.entry_name.get()
        dimensionality = self.entry_dimensionality.get()
        description = self.entry_description.get()
        anion_stoich = self.entry_anion_stoich.get()

        try:
            dimensionality = int(dimensionality)
            anion_stoich = int(anion_stoich)
        except:
            tk.messagebox.showerror(title="error", message="dimensionality and stoichiometry must be integer numbers")

        try:
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Phase_templates
                                                  (id INTEGER PRIMARY KEY,
                                                  name TEXT,
                                                  description TEXT NULL,
                                                  anion_stoichiometry INT,
                                                  dimensionality INT)
                                          '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Phase_template WHERE name = ? LIMIT 1", (name, ))
            if cursor.fetchone():
                mb.showerror(title="error", message="Phase template with this name already exists")
                return
            else:
                # Insert Data
                data_insert_query = '''INSERT INTO Phase_templates
                                                       (name, description, anion_stoichiometry, dimensionality) VALUES
                                                       (?, ?, ?, ?)'''
                data_insert_tuple = (name, description, anion_stoich, dimensionality)
                cursor.execute(data_insert_query, data_insert_tuple)

                conn.commit()
                conn.close()

                mb.showinfo(title="success", message=f"template successfully upload")

                self.entry_name.delete(0, tk.END)
                self.entry_dimensionality.delete(0, tk.END)
                self.entry_description.delete(0, tk.END)
                self.entry_anion_stoich.delete(0, tk.END)

        except TypeError:
            mb.showerror(title="error", message="Error: Invalid type operation!")
            return

    def enter_elements(self):
        id_template = self.return_id()
        for element in self.element_frames:
            stoich, valence = element.get_data()
            try:
                conn = sqlite3.connect('data.db')
                table_create_query = '''CREATE TABLE IF NOT EXISTS Template_sites
                                           (id_phase TEXT,
                                           stoichiometry INT,
                                           type TEXT,
                                           valence TEXT,
                                           name_candidate TEXT NULL,
                                           FOREIGN KEY (id_phase) REFERENCES Phase_templates (id),
                                           FOREIGN KEY (name_candidate) REFERENCES Candidate_cations (name))
                                   '''
                conn.execute(table_create_query)
                cursor = conn.cursor()
                name_candidate = self.text+"_val_"+valence
                data_insert_query = '''INSERT INTO Template_sites 
                                        (id_phase, stoichiometry, type, valence, name_candidate) VALUES
                                         (?, ?, ?, ?, ?)'''
                data_insert_tuple = (id_template, stoich, self.text, valence, name_candidate)
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()

            except TypeError:
                mb.showerror(title="error", message="Error: Invalid type operation!")
                return