import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from collections import namedtuple
from gui.comp_forma_models import CompositionStructureModel
import sqlite3

Numbers = namedtuple("Numbers", ["elements", "solvent"])

class Solvents(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text="Solvents")
        self.controller = controller

        type = tk.Label(self, text="type")
        self.type_box = ttk.Combobox(self, values=["solvent", "antisolvent"])
        type.grid(row=0, column=0)
        self.type_box.grid(row=1, column=0)

        symbol = tk.Label(self, text="symbol")
        self.entry_symbol = tk.Entry(self)
        symbol.grid(row=0, column=1)
        self.entry_symbol.grid(row=1, column=1)

        fraction = tk.Label(self, text="fraction")
        self.entry_fraction = tk.Entry(self)
        fraction.grid(row=0, column=2)
        self.entry_fraction.grid(row=1, column=2)

    def get_fractions(self):
        solvent_type = self.type_box.get()
        fraction = self.entry_fraction.get()

        try:
            fraction = float(fraction)
        except ValueError:
            mb.showerror(title="error", message="fraction must be float number")
            return

        if solvent_type == "solvent":
            return fraction, 0
        else:
            return 0, fraction

    def get_data(self, id_info):
        solvent_type = self.type_box.get()
        symbol = self.entry_symbol.get()
        fraction = self.entry_fraction.get()

        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Solvents WHERE name = (?)", (symbol))
            if cursor.fetchone():
                cursor.close()
                table_create_query = '''CREATE TABLE IF NOT EXISTS Compositions_solvents
                                                                   (id INTEGER PRIMARY KEY,
                                                                    id_info INT NULL,
                                                                    solvent_type TEXT, 
                                                                    symbol TEXT, 
                                                                    fraction FLOAT,
                                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id),
                                                                    FOREIGN KEY (symbol) REFERENCES Solvents (name))'''
                conn.execute(table_create_query)
                cursor = conn.cursor()
                # Insert Data
                data_insert_query = '''INSERT INTO Compositions_solvents 
                                        (id_info, solvent_type, symbol, fraction) VALUES 
                                        (?, ?, ?, ?)'''
                data_insert_tuple = (id_info, solvent_type, symbol, fraction)
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()

                self.type_box.delete(0, tk.END)
                self.entry_symbol.delete(0, tk.END)
                self.entry_fraction.delete(0, tk.END)
            else:
                mb.showerror(title="error", message=f"solvent {symbol} doesn't exist in database")
                return
        except TypeError:
            mb.showerror(title="error", message="Error: Invalid type operation!")
            return

        finally:
            conn.close()

class CompositionInformation(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text="Composition information")
        self.controller = controller

        doi = tk.Label(self, text="doi")
        self.entry_doi = tk.Entry(self)
        doi.grid(row=0, column=0)
        self.entry_doi.grid(row=1, column=0)

        data_type = tk.Label(self, text="data type")
        self.data_box = ttk.Combobox(self, values=["", "experimental", "theoretical", "modelling"])
        data_type.grid(row=0, column=1)
        self.data_box.grid(row=1, column=1)

        notes = tk.Label(self, text="notes")
        self.entry_notes = tk.Entry(self)
        notes.grid(row=0, column=2)
        self.entry_notes.grid(row=1, column=2)

        num_elements = tk.Label(self, text="number of elements")
        self.entry_num_elements = tk.Entry(self)
        num_elements.grid(row=2, column=0)
        self.entry_num_elements.grid(row=3, column=0)

        num_solv = tk.Label(self, text="number of solvents")
        self.entry_num_solv = tk.Entry(self)
        num_solv.grid(row=2, column=1)
        self.entry_num_solv.grid(row=3, column=1)

    def get_data(self):
        doi = self.entry_doi.get()
        data_type = self.data_box.get()
        notes = self.entry_notes.get()

        try:
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Compositions_info 
                                       (id INTEGER PRIMARY KEY,
                                       name TEXT NULL, 
                                       doi TEXT NULL,
                                       data_type TEXT NULL, 
                                       notes TEXT)
                               '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            # Insert Data
            data_insert_query = '''INSERT INTO Compositions_info  
                                                    (doi, data_type, notes) VALUES 
                                                    (?, ?, ?)'''
            data_insert_tuple = (doi, data_type, notes)
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            mb.showinfo(title="success", message="Composition registered. Please fill another requirement fields")


        except TypeError:
            mb.showerror(title="error", message="Error: Invalid type operation!")
            return

        finally:
            conn.close()

    def delete_data(self):
        self.entry_doi.delete(0, tk.END)
        self.data_box.delete(0, tk.END)
        self.entry_notes.delete(0, tk.END)
        self.entry_num_elements.delete(0, tk.END)
        self.entry_num_solv.delete(0, tk.END)

    def return_id(self):
        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.execute("SELECT id FROM Compositions_info ORDER BY id DESC LIMIT 1")
            id_info = cursor.fetchone()
        finally:
            conn.close()
        return id_info[0]

    def get_numbers(self):
        elements = self.entry_num_elements.get()
        solvents = self.entry_num_solv.get()

        try:
            elements = int(elements) if elements else 0
            solvents = int(solvents) if solvents else 0
        except ValueError:
            mb.showerror(title="error", message="number of elements or solvents must be integer numbers")
            return
        elements = int(elements)
        solvents = int(solvents)
        return Numbers(elements, solvents)

class CompositionStructure(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text="Composition structure")
        self.controller = controller

        structure_type = tk.Label(self, text="structure type")
        self.structure_box = ttk.Combobox(self, values=["A_site", "B_site", "B_double", "anion"])
        structure_type.grid(row=0, column=0)
        self.structure_box.grid(row=1, column=0)

        symbol = tk.Label(self, text="symbol")
        self.entry_symbol = tk.Entry(self)
        symbol.grid(row=0, column=1)
        self.entry_symbol.grid(row=1, column=1)

        fraction = tk.Label(self, text="fraction")
        self.entry_fraction = tk.Entry(self)
        fraction.grid(row=0, column=2)
        self.entry_fraction.grid(row=1, column=2)

        valence = tk.Label(self, text="valence")
        self.entry_valence = tk.Entry(self)
        valence.grid(row=0, column=3)
        self.entry_valence.grid(row=1, column=3)

    def get_fractions(self):
        structure_type = self.structure_box.get()
        valence = self.entry_valence.get()
        fraction = self.entry_fraction.get()
        try:
            fraction = float(fraction)
        except ValueError:
            mb.showerror(title="error", message="fraction must be float number")
            return
        try:
            valence = int(valence)
        except ValueError:
            mb.showerror(title="error", message="valence must be integer number")
            return

        if structure_type == "A_site":
            return fraction, 0, 0, 0
        elif structure_type == "B_site":
            return 0, fraction, 0, 0
        elif structure_type == "B_double":
            return 0, 0, fraction, 0
        else:
            return 0, 0, 0, fraction

    def get_data(self, id_info):
        structure_type = self.structure_box.get()
        symbol = self.entry_symbol.get()
        fraction = self.entry_fraction.get()
        valence = self.entry_valence.get()

        if structure_type == "anion":
            ion_type = "anion"
        else:
            ion_type = "cation"

        try:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? AND ion_type = ?", (symbol, ion_type))
            if cursor.fetchone():
                cursor.close()
                table_create_query = '''CREATE TABLE IF NOT EXISTS Compositions_structure 
                                                       (id INTEGER PRIMARY KEY,
                                                        id_info INT NULL,
                                                        structure_type TEXT, 
                                                        symbol TEXT, 
                                                        fraction FLOAT,
                                                        valence FLOAT,
                                                        FOREIGN KEY (id_info) REFERENCES Compositions_info (id),
                                                        FOREIGN KEY (symbol) REFERENCES Ions (name))'''
                conn.execute(table_create_query)
                cursor = conn.cursor()
                # Insert Data
                data_insert_query = '''INSERT INTO Compositions_structure 
                                                                    (id_info, structure_type, symbol, fraction, valence) VALUES 
                                                                    (?, ?, ?, ?, ?)'''
                data_insert_tuple = (id_info, structure_type, symbol, fraction, valence)
                cursor.execute(data_insert_query, data_insert_tuple)
                conn.commit()

                self.structure_box.delete(0, tk.END)
                self.entry_symbol.delete(0, tk.END)
                self.entry_fraction.delete(0, tk.END)
                self.entry_valence.delete(0, tk.END)
            else:
                mb.showerror(title="error", message=f"ion {symbol} doesn't exist in database")
                return

        except TypeError:
            mb.showerror(title="error", message="Error: Invalid type operation!")
            return

        finally:
            conn.close()

class Properties(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text = "Properties")
        self.controller = controller

        bg = tk.Label(self, text="band gap, eV")
        self.entry_bg = tk.Entry(self)
        bg.grid(row=0, column=0)
        self.entry_bg.grid(row=1, column=0)

        pp = tk.Label(self, text="pce percent")
        self.entry_pp = tk.Entry(self)
        pp.grid(row=0, column=1)
        self.entry_pp.grid(row=1, column=1)

        voc = tk.Label(self, text="voc, V")
        self.entry_voc = tk.Entry(self)
        voc.grid(row=0, column=2)
        self.entry_voc.grid(row=1, column=2)

        jsc = tk.Label(self, text="jsc, mA/cm^2")
        self.entry_jsc = tk.Entry(self)
        jsc.grid(row=2, column=0)
        self.entry_jsc.grid(row=3, column=0)

        ff_percent = tk.Label(self, text="ff percent")
        self.entry_ff_percent = tk.Entry(self)
        ff_percent.grid(row=2, column=1)
        self.entry_ff_percent.grid(row=3, column=1)

        stability_notes = tk.Label(self, text="stability notes")
        self.entry_stability_notes = tk.Entry(self)
        stability_notes.grid(row=2, column=2)
        self.entry_stability_notes.grid(row=3, column=2)


    def get_data(self, id_info):
        band_gap = self.entry_bg.get()
        ff_percent = self.entry_ff_percent.get()
        pce_percent = self.entry_pp.get()
        voc = self.entry_voc.get()
        jsc = self.entry_jsc.get()
        stability_notes = self.entry_stability_notes.get()

        try:
            conn = sqlite3.connect('data.db')
            table_create_query = '''CREATE TABLE IF NOT EXISTS Compositions_properties 
                                               (id INTEGER PRIMARY KEY,
                                               id_info INT NULL,
                                               band_gap FLOAT NULL, 
                                               ff_percent FLOAT NULL, 
                                               pce_percent FLOAT NULL,
                                               voc FLOAT NULL,
                                               jsc FLOAT NULL,  
                                               stability_notes TEXT NULL,
                                               v_antisolvent FLOAT NULL,
                                               anion_stoichiometry FLOAT NULL,
                                               FOREIGN KEY (id_info) REFERENCES Compositions_info (id))
                                       '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            # Insert Data
            data_insert_query = '''INSERT INTO Compositions_properties 
                                                            (id_info, band_gap, ff_percent, pce_percent, voc, jsc, stability_notes) VALUES 
                                                            (?, ?, ?, ?, ?, ?, ?)'''
            data_insert_tuple = (id_info, band_gap, ff_percent, pce_percent, voc, jsc, stability_notes)
            conn.execute(data_insert_query, data_insert_tuple)
            conn.commit()

            self.entry_bg.delete(0, tk.END)
            self.entry_ff_percent.delete(0, tk.END)
            self.entry_pp.delete(0, tk.END)
            self.entry_voc.delete(0, tk.END)
            self.entry_jsc.delete(0, tk.END)
            self.entry_stability_notes.delete(0, tk.END)

        except TypeError:
            mb.showerror(title="error", message="Error: Invalid type operation!")
            return

        finally:
            conn.close()

class AddCompositionForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new composition")

        container = tk.Frame(self, padx=20, pady=20)
        container.pack(expand=True, fill='both')

        self.first_column = ttk.Frame(container)
        self.sec_column = ttk.Frame(container)
        self.third_column = ttk.Frame(container)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill='x', pady=10)

        self.first_column.pack(side='left', fill='both', expand=True, padx=5)
        self.sec_column.pack(side='left', fill='both', expand=True, padx=5)
        self.third_column.pack(side='left', fill='both', expand=True, padx=5)

        self.composition_info = CompositionInformation(self.first_column, self)
        self.first_button = tk.Button(self.first_column, text = "Enter info",
                                      command=lambda: self.numbers_data(self.first_column, self.sec_column, self.third_column, self.button_frame))

        self.composition_info.pack(fill='x', pady=5)
        self.first_button.pack(fill='x', pady=5)

        #хранение всех виджетов возникающих автоматически, хранение id основной таблицы
        self.composition_structures = []
        self.solvents = []
        self.properties = object
        self.main_button = object

    def numbers_data(self, column1, column2, column3, button_frame):
        # создаем необходимое количество виджетов для расторителей и элементов
        numbers = self.composition_info.get_numbers()
        num_solv = numbers.solvent
        num_elem = numbers.elements
        for i in range(num_elem):
            widget = CompositionStructure(column2, self)
            widget.pack(fill='x', pady=5)
            self.composition_structures.append(widget)
        for i in range(num_solv):
            widget = Solvents(column3, self)
            widget.pack(fill='x', pady=5)
            self.solvents.append(widget)
        self.v_antisolvent = tk.Label(self.third_column, text="V antisolvent")
        self.v_antisolvent_entry = tk.Entry(self.third_column)
        self.tot_anion_s = tk.Label(self.sec_column, text="total anion stoichiometry")
        self.tot_anion_s_entry = tk.Entry(self.sec_column)
        self.v_antisolvent.pack(fill='x', pady=5)
        self.tot_anion_s.pack(fill='x', pady=5)
        self.v_antisolvent_entry.pack(fill='x', pady=5)
        self.tot_anion_s_entry.pack(fill='x', pady=5)
        # заполняем основную табличку
        self.composition_info.get_data()
        # получаем id основной таблицы
        id = self.composition_info.return_id()
        # добавляем properties
        self.properties = Properties(column1, self)
        self.properties.pack(fill='x', pady=5)
        self.first_button.destroy()
        self.main_button = tk.Button(button_frame, text="Enter data", command=lambda: self.get_all_data(id))
        self.main_button.pack(fill='x', pady=5)

    def get_all_data(self, id_info):

        fractions1 = [0]*2
        for element in self.solvents:
            fractions2 = element.get_fractions()
            for i in range(2):
                fractions1[i] += fractions2[i]
                print(fractions1[i])
        for num in fractions1:
            if 0.99 <= num <= 1.01 or num == 0:
                pass
            else:
                mb.showerror(title="error", message="fraction summ for one type solvents must be 1")
                return

        fractions1 = [0] * 4
        for element in self.composition_structures:
            fractions2 = element.get_fractions()
            for i in range(4):
                fractions1[i] += fractions2[i]
                print(fractions1[i])
        for num in fractions1:
            if 0.99 <= num <= 1.01 or num == 0:
                pass
            else:
                mb.showerror(title="error", message="fraction summ for one type elements must be 1")
                return
        for element in self.solvents:
            element.get_data(id_info)
        for element in self.composition_structures:
            element.get_data(id_info)
        conn = None
        try:
            # get solvents and elements table

            # get properties table
            self.properties.get_data(id_info)

            conn = sqlite3.connect('data.db')
            # Update properties table
            data_update_query = '''UPDATE Compositions_properties  SET v_antisolvent = ?,  anion_stoichiometry = ?
                                            WHERE id = ?'''
            data_update_tuple = (self.v_antisolvent_entry.get(), self.tot_anion_s_entry.get(), id_info)
            conn.execute(data_update_query, data_update_tuple)
            conn.commit()

            self.v_antisolvent_entry.delete(0, tk.END)
            self.tot_anion_s_entry.delete(0, tk.END)
            self.composition_info.delete_data()
            mb.showinfo(title="success", message="Composition added in database")

        except TypeError:
            mb.showerror(title="error", message="Error: Invalid type operation!")
            return

        finally:
            if conn:
                conn.close()

