import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
#from comp_forma_models import CompositionInformation, CompositionStructure, Solvents, Properties

class CompositionInformation(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.LabelFrame(self, text="Composition information")
        label.grid(row=0, column=0, padx=20, pady=10)

        doi = tk.Label(label, text="doi")
        entry_doi = tk.Entry(label)
        doi.grid(row=0, column=0)
        entry_doi.grid(row=1, column=0)

        data_type = tk.Label(label, text="data type")
        data_box = ttk.Combobox(label, values=["", "experimental", "theoretical", "modelling"])
        data_type.grid(row=0, column=1)
        data_box.grid(row=1, column=1)

        notes = tk.Label(label, text="notes")
        entry_notes = tk.Entry(label)
        notes.grid(row=0, column=2)
        entry_notes.grid(row=1, column=2)

class CompositionStructure(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.LabelFrame(self, text="Composition structure")
        label.grid(row=0, column=0, padx=20, pady=10)

        structure_type = tk.Label(label, text="structure type")
        structure_box = ttk.Combobox(label, values=["A_site", "B_site", "B_double", "anion"])
        structure_type.grid(row=0, column=0)
        structure_box.grid(row=1, column=0)

        symbol = tk.Label(label, text="symbol")
        symbol_entry = tk.Entry(label)
        symbol.grid(row=0, column=1)
        symbol_entry.grid(row=1, column=1)

        fraction = tk.Label(label, text="fraction")
        fraction_entry = tk.Entry(label)
        fraction.grid(row=0, column=2)
        fraction_entry.grid(row=1, column=2)

        valence = tk.Label(label, text="valence")
        valence_entry = tk.Entry(label)
        valence.grid(row=2, column=1)
        valence_entry.grid(row=3, column=1)


class Solvents(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        solv_frame = tk.LabelFrame(self, text="Solvents")
        solv_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        type = tk.Label(solv_frame, text="type")
        type_box = ttk.Combobox(solv_frame, values=["solvent", "antisolvent"])
        type.grid(row=0, column=0)
        type_box.grid(row=1, column=0)

        symbol = tk.Label(solv_frame, text="symbol")
        symbol_entry = tk.Entry(solv_frame)
        symbol.grid(row=0, column=1)
        symbol_entry.grid(row=1, column=1)

        fraction = tk.Label(solv_frame, text="fraction")
        fraction_entry = tk.Entry(solv_frame)
        fraction.grid(row=0, column=2)
        fraction_entry.grid(row=1, column=2)

class Properties(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        properties_frame = tk.LabelFrame(self, text="Properties")
        properties_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        bg = tk.Label(properties_frame, text="band gap, eV")
        bg_entry = tk.Entry(properties_frame)
        bg.grid(row=0, column=0)
        bg_entry.grid(row=1, column=0)

        pp = tk.Label(properties_frame, text="pce percent")
        pp_entry = tk.Entry(properties_frame)
        pp.grid(row=0, column=1)
        pp_entry.grid(row=1, column=1)

        voc = tk.Label(properties_frame, text="voc, V")
        voc_entry = tk.Entry(properties_frame)
        voc.grid(row=0, column=2)
        voc_entry.grid(row=1, column=2)

        jsc = tk.Label(properties_frame, text="jsc, mA/cm^2")
        jsc_entry = tk.Entry(properties_frame)
        jsc.grid(row=2, column=0)
        jsc_entry.grid(row=3, column=0)

        ff_percent = tk.Label(properties_frame, text="ff percent")
        ff_percent_entry = tk.Entry(properties_frame)
        ff_percent.grid(row=2, column=1)
        ff_percent_entry.grid(row=3, column=1)

        stability_notes = tk.Label(properties_frame, text="stability notes")
        stability_notes_entry = tk.Entry(properties_frame)
        stability_notes.grid(row=2, column=2)
        stability_notes_entry.grid(row=3, column=2)

class AddCompositionForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add new composition")

        self.container = ttk.Frame(self)
        self.container.pack(anchor="w", fill = tk.Y)
        # self.container.grid_rowconfigure(0, weight=1)
        # self.container.grid_columnconfigure(0, weight=1)
        # self.container.bind("<Configure>", self._resize_window)

        self.sec_cont = ttk.Frame(self)
        self.sec_cont.pack(anchor="center", fill = tk.Y)

        self.third_cont = ttk.Frame(self)
        self.third_cont.pack(anchor="e", fill = tk.Y)

        self.composition_info = CompositionInformation(self.container, self)
        self.composition_structure = CompositionStructure(self.sec_cont, self)
        self.solvents = Solvents(self.third_cont, self)
        self.properties = Properties(self.container, self)
        self.button = tk.Button(self.container, text="Enter data")

        self.composition_info.grid(row=0, column=0, sticky="ns")
        self.composition_structure.grid(row=0, column=1,sticky="ns")
        self.solvents.grid(row=0, column=2, sticky="ns")
        self.properties.grid(row=1, column=0, sticky="ns")
        self.button.grid(row=2, column=0, sticky="ns")

    # def _resize_window(self, event=None):
    #     self.update_idletasks()
    #     req_width = self.container.winfo_reqwidth()
    #     req_height = self.container.winfo_reqheight()
    #     self.geometry(f"{req_width}x{req_height}")
    #
    # def open(self):
    #     self.grab_set()
    #     self.wait_window()
    #     username = self.username.get()
    #     password = self.password.get()
    #     return User(username, password, self.user_type)

# class CompositionStructureForm(tk.LabelFrame):
#     fields = ("site", "symbol", "fraction", "valence")
#
#     def __init__(self, master, **kwargs):
#         super().__init__(master, text="Composition structure", padx=10, pady=10, **kwargs)
#         self.frame = tk.Frame(self)
#         self.entries = list(map(self.create_field, enumerate(self.fields)))
#         self.frame.pack()
#
#     def create_field(self, field):
#         position, text = field
#         label = tk.Label(self.frame, text=text)
#         entry = tk.Entry(self.frame, width=25)
#         label.grid(row=position, column=0, pady=5)
#         entry.grid(row=position, column=1, pady=5)
#         return entry
#
#     def get_details(self):
#         values = [e.get() for e in self.entries]
#         try:
#             return CompositionStructure(*values)
#         except ValueError as e:
#             mb.showerror("Ошибка валидации", str(e), parent=self)
#
# class SolventsForm(tk.LabelFrame):
#     fields = ("type", "symbol", "fraction")
#
#     def __init__(self, master, **kwargs):
#         super().__init__(master, text="Composition structure", padx=10, pady=10, **kwargs)
#         self.frame = tk.Frame(self)
#         self.entries = list(map(self.create_field, enumerate(self.fields)))
#         self.frame.pack()
#
#     def create_field(self, field):
#         position, text = field
#         label = tk.Label(self.frame, text=text)
#         entry = tk.Entry(self.frame, width=25)
#         label.grid(row=position, column=0, pady=5)
#         entry.grid(row=position, column=1, pady=5)
#         return entry
#
#     def get_details(self):
#         values = [e.get() for e in self.entries]
#         try:
#             return Solvents(*values)
#         except ValueError as e:
#             mb.showerror("Ошибка валидации", str(e), parent=self)
#
#
#
# # Button
# button = tk.Button(frame, text="Enter data", command=enter_data)
# button.grid(row=5, column=0, sticky="news", padx=20, pady=10)
#
# window.mainloop()