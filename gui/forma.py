import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from collections import namedtuple

Numbers = namedtuple("Numbers", ["elements", "solvent"])

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
        data_box = self.data_box.get()
        notes = self.entry_notes.get()
        elements = self.entry_num_elements.get()
        solvents = self.entry_num_solv.get()

        try:
            elements = int(elements) if elements else 0
            solvents = int(solvents) if solvents else 0
        except ValueError:
            # Можно добавить обработку ошибки, например:
            raise ValueError("Number of elements and solvents must be integers")

        elements = int(elements)
        solvents = int(solvents)

        return Numbers(elements, solvents)

class CompositionStructure(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text="Composition structure")
        self.controller = controller

        structure_type = tk.Label(self, text="structure type")
        structure_box = ttk.Combobox(self, values=["A_site", "B_site", "B_double", "anion"])
        structure_type.grid(row=0, column=0)
        structure_box.grid(row=1, column=0)

        symbol = tk.Label(self, text="symbol")
        symbol_entry = tk.Entry(self)
        symbol.grid(row=0, column=1)
        symbol_entry.grid(row=1, column=1)

        fraction = tk.Label(self, text="fraction")
        fraction_entry = tk.Entry(self)
        fraction.grid(row=0, column=2)
        fraction_entry.grid(row=1, column=2)

        valence = tk.Label(self, text="valence")
        valence_entry = tk.Entry(self)
        valence.grid(row=0, column=3)
        valence_entry.grid(row=1, column=3)


class Solvents(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text="Solvents")
        self.controller = controller

        type = tk.Label(self, text="type")
        type_box = ttk.Combobox(self, values=["solvent", "antisolvent"])
        type.grid(row=0, column=0)
        type_box.grid(row=1, column=0)

        symbol = tk.Label(self, text="symbol")
        symbol_entry = tk.Entry(self)
        symbol.grid(row=0, column=1)
        symbol_entry.grid(row=1, column=1)

        fraction = tk.Label(self, text="fraction")
        fraction_entry = tk.Entry(self)
        fraction.grid(row=0, column=2)
        fraction_entry.grid(row=1, column=2)

class Properties(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, text = "Properties")
        self.controller = controller

        bg = tk.Label(self, text="band gap, eV")
        bg_entry = tk.Entry(self)
        bg.grid(row=0, column=0)
        bg_entry.grid(row=1, column=0)

        pp = tk.Label(self, text="pce percent")
        pp_entry = tk.Entry(self)
        pp.grid(row=0, column=1)
        pp_entry.grid(row=1, column=1)

        voc = tk.Label(self, text="voc, V")
        voc_entry = tk.Entry(self)
        voc.grid(row=0, column=2)
        voc_entry.grid(row=1, column=2)

        jsc = tk.Label(self, text="jsc, mA/cm^2")
        jsc_entry = tk.Entry(self)
        jsc.grid(row=2, column=0)
        jsc_entry.grid(row=3, column=0)

        ff_percent = tk.Label(self, text="ff percent")
        ff_percent_entry = tk.Entry(self)
        ff_percent.grid(row=2, column=1)
        ff_percent_entry.grid(row=3, column=1)

        stability_notes = tk.Label(self, text="stability notes")
        stability_notes_entry = tk.Entry(self)
        stability_notes.grid(row=2, column=2)
        stability_notes_entry.grid(row=3, column=2)

class AddCompositionForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new composition")

        container = tk.Frame(self, padx=20, pady=20)
        container.pack(expand=True, fill='both')

        self.first_column = ttk.Frame(container)
        self.sec_column = ttk.Frame(container)
        self.third_column = ttk.Frame(container)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', pady=10)

        self.first_column.pack(side='left', fill='both', expand=True, padx=5)
        self.sec_column.pack(side='left', fill='both', expand=True, padx=5)
        self.third_column.pack(side='left', fill='both', expand=True, padx=5)

        self.composition_info = CompositionInformation(self.first_column, self)
        self.properties = Properties(self.first_column, self)
        self.first_button = tk.Button(self.first_column, text = "Enter info",
                                      command=lambda: self.numbers_data(self.sec_column, self.third_column))
        self.button = tk.Button(button_frame, text="Enter data")

        self.composition_info.pack(fill='x', pady=5)
        self.properties.pack(fill='x', pady=5)
        self.first_button.pack(fill='x', pady=5)
        self.button.pack(fill='x', pady=5)

    def numbers_data(self, column2, column3):
        numbers = self.composition_info.get_data()
        num_solv = numbers.solvent
        num_elem = numbers.elements
        print(num_solv)
        for i in range(num_elem):
            self.composition_structure = CompositionStructure(column2, self)
            self.composition_structure.pack(fill='x', pady=5)
        for i in range(num_solv):
            self.solvents = Solvents(column3, self)
            self.solvents.pack(fill='x', pady=5)