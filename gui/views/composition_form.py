import tkinter as tk
from tkinter import ttk

import analysis
from analysis import get_templates_list

class CompositionView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Add new composition")
        self.build_ui()
        self.dynamic_widgets = []

    def build_ui(self):
        self.container = tk.Frame(self, padx=10, pady=10)
        self.container.pack(expand=True, fill='both')

        self.first_column = self.create_scrollable_frame(self.container, show_scrollbar=False)
        self.sec_column = self.create_scrollable_frame(self.container, show_scrollbar=False)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill='x', pady=10)

        self.first_column.pack(side='left', fill='both', expand=True)
        self.sec_column.pack(side='left', fill='both', expand=True)

        self.create_info_frame()
        self.first_button = tk.Button(
            self.first_column.inner_frame,
            text="Enter info",
            command=self.on_info_submit
        )
        self.first_button.pack(fill='x', pady=5)

    def create_scrollable_frame(self, parent, show_scrollbar=False):
        container = tk.Frame(parent)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)

        if show_scrollbar:
            scrollbar.pack(side="right", fill="y")

        container.canvas = canvas
        container.scrollbar = scrollbar
        container.inner_frame = scrollable_frame
        container.show_scrollbar = lambda: scrollbar.pack(side="right", fill="y")
        container.hide_scrollbar = lambda: scrollbar.pack_forget()

        return container

    def create_info_frame(self):
        info_frame = tk.LabelFrame(self.first_column.inner_frame,
                                   text="Composition information")  # Изменено на inner_frame
        info_frame.pack(side="top", fill='x', padx=5, pady=5)

        tk.Label(info_frame, text="doi").grid(row=0, column=0)
        self.entry_doi = tk.Entry(info_frame)
        self.entry_doi.grid(row=1, column=0)

        tk.Label(info_frame, text="data type").grid(row=0, column=1)
        self.data_box = ttk.Combobox(info_frame, values=["", "experimental", "theoretical", "modelling"])
        self.data_box.grid(row=1, column=1)

        tk.Label(info_frame, text="notes").grid(row=0, column=2)
        self.entry_notes = tk.Entry(info_frame)
        self.entry_notes.grid(row=1, column=2)

        phase_t = get_templates_list()

        tk.Label(info_frame, text="phase template").grid(row=2, column=0)
        self.phase_template = ttk.Combobox(info_frame, values = phase_t)
        self.phase_template.grid(row=3, column=0)

        tk.Label(info_frame, text="number of elements").grid(row=2, column=1)
        self.entry_num_elements = tk.Entry(info_frame)
        self.entry_num_elements.grid(row=3, column=1)

        tk.Label(info_frame, text="number of solvents").grid(row=2, column=2)
        self.entry_num_solv = tk.Entry(info_frame)
        self.entry_num_solv.grid(row=3, column=2)

        tk.Label(info_frame, text="number of k-factors").grid(row=4, column=1)
        self.entry_k_fact = tk.Entry(info_frame)
        self.entry_k_fact.grid(row=5, column=1)

    def clear_dynamic_widgets(self):
        for widget_info in self.dynamic_widgets:
                widget_info['frame'].destroy()

        self.dynamic_widgets = []

    def create_dynamic_widgets(self, num_elements, num_solvents, num_k):

        self.clear_dynamic_widgets()

        self.tot_anion_s_label = tk.Label(self.sec_column.inner_frame, text="total anion stoichiometry")
        self.tot_anion_s_label.pack(fill='x')
        self.tot_anion_s_entry = tk.Entry(self.sec_column.inner_frame)
        self.tot_anion_s_entry.pack(fill='x')

        struct_frame = tk.LabelFrame(self.sec_column.inner_frame, text = "structure")
        struct_frame.pack(side="top", fill='x', padx=5, pady=5)

        struct_frame.columnconfigure(0, weight=1)
        struct_frame.columnconfigure(1, weight=1)
        struct_frame.columnconfigure(2, weight=1)
        struct_frame.columnconfigure(3, weight=1)

        tk.Label(struct_frame, text="structure type").grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        tk.Label(struct_frame, text="symbol").grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        tk.Label(struct_frame, text="fraction").grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        tk.Label(struct_frame, text="valence").grid(row=0, column=3, sticky="ew", padx=2, pady=2)

        for i in range(num_elements):

            structure_box = ttk.Combobox(struct_frame, values=["A_site", "B_site", "B_double", "spacer_site", "anion"])
            structure_box.grid(row=i+1, column=0, sticky="ew", padx=2, pady=2)

            entry_symbol = tk.Entry(struct_frame)
            entry_symbol.grid(row=i+1, column=1, sticky="ew", padx=2, pady=2)

            entry_fraction = tk.Entry(struct_frame)
            entry_fraction.grid(row=i+1, column=2, sticky="ew", padx=2, pady=2)

            entry_valence = tk.Entry(struct_frame)
            entry_valence.grid(row=i+1, column=3, sticky="ew", padx=2, pady=2)

            self.dynamic_widgets.append({
                'frame': struct_frame,
                'type': 'structure',
                'widgets': {
                    'structure_type': structure_box,
                    'symbol': entry_symbol,
                    'fraction': entry_fraction,
                    'valence': entry_valence
                }
            })

        self.v_solution_label = tk.Label(self.sec_column.inner_frame, text="V solution")
        self.v_solution_label.pack(fill='x')
        self.v_solution_entry = tk.Entry(self.sec_column.inner_frame)
        self.v_solution_entry.pack(fill='x')

        self.c_solution_label = tk.Label(self.sec_column.inner_frame, text="C solution")
        self.c_solution_label.pack(fill='x')
        self.c_solution_entry = tk.Entry(self.sec_column.inner_frame)
        self.c_solution_entry.pack(fill='x')

        self.v_antisolvent_label = tk.Label(self.sec_column.inner_frame, text="V antisolvent")
        self.v_antisolvent_label.pack(fill='x')
        self.v_antisolvent_entry = tk.Entry(self.sec_column.inner_frame)
        self.v_antisolvent_entry.pack(fill='x')

        solv_frame = tk.LabelFrame(self.sec_column.inner_frame, text = "solvents")
        solv_frame.pack(side="top", fill='x', padx=5, pady=5)

        solv_frame.columnconfigure(0, weight=1)
        solv_frame.columnconfigure(1, weight=1)
        solv_frame.columnconfigure(2, weight=1)

        tk.Label(solv_frame, text="type").grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        tk.Label(solv_frame, text="symbol").grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        tk.Label(solv_frame, text="fraction").grid(row=0, column=2, sticky="ew", padx=2, pady=2)

        for i in range(num_solvents):

            type_box = ttk.Combobox(solv_frame, values=["solvent", "antisolvent"])
            type_box.grid(row=i+1, column=0, sticky="ew", padx=2, pady=2)

            entry_symbol = tk.Entry(solv_frame)
            entry_symbol.grid(row=i+1, column=1, sticky="ew", padx=2, pady=2)

            entry_fraction = tk.Entry(solv_frame)
            entry_fraction.grid(row=i+1, column=2, sticky="ew", padx=2, pady=2)

            self.dynamic_widgets.append({
                'frame': solv_frame,
                'type': 'solvent',
                'widgets': {
                    'solvent_type': type_box,
                    'symbol': entry_symbol,
                    'fraction': entry_fraction
                }
            })
        self.method_description_label = tk.Label(self.sec_column.inner_frame, text="method_description")
        self.method_description_label.pack(fill='x')
        self.method_description_entry = tk.Entry(self.sec_column.inner_frame)
        self.method_description_entry.pack(fill='x')

        properties_frame = tk.LabelFrame(self.first_column.inner_frame, text="Properties")
        properties_frame.pack(side="top", fill='x')

        tk.Label(properties_frame, text="band gap, eV").grid(row=0, column=0)
        self.entry_bg = tk.Entry(properties_frame)
        self.entry_bg.grid(row=1, column=0)

        tk.Label(properties_frame, text="pce percent").grid(row=0, column=1)
        self.entry_pp = tk.Entry(properties_frame)
        self.entry_pp.grid(row=1, column=1)

        tk.Label(properties_frame, text="voc, V").grid(row=0, column=2)
        self.entry_voc = tk.Entry(properties_frame)
        self.entry_voc.grid(row=1, column=2)

        tk.Label(properties_frame, text="jsc, mA/cm^2").grid(row=2, column=0)
        self.entry_jsc = tk.Entry(properties_frame)
        self.entry_jsc.grid(row=3, column=0)

        tk.Label(properties_frame, text="ff percent").grid(row=2, column=1)
        self.entry_ff_percent = tk.Entry(properties_frame)
        self.entry_ff_percent.grid(row=3, column=1)

        tk.Label(properties_frame, text="stability notes").grid(row=2, column=2)
        self.entry_stability_notes = tk.Entry(properties_frame)
        self.entry_stability_notes.grid(row=3, column=2)

        k_frame = tk.LabelFrame(self.first_column.inner_frame, text = "k-factors")
        k_frame.pack(side="top", fill='x', padx=5, pady=5)

        k_frame.columnconfigure(0, weight=1)
        k_frame.columnconfigure(1, weight=1)

        tk.Label(k_frame, text="precursor").grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        tk.Label(k_frame, text="k-factor").grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        for i in range(num_k):

            entry_precursor = tk.Entry(k_frame)
            entry_precursor.grid(row=i+1, column=0, sticky="ew", padx=2, pady=2)

            entry_k_factor = tk.Entry(k_frame)
            entry_k_factor.grid(row=i+1, column=1, sticky="ew", padx=2, pady=2)

            self.dynamic_widgets.append({
                'frame': k_frame,
                'type': 'k_factors',
                'widgets': {
                    'precursor': entry_precursor,
                    'k_factor': entry_k_factor,
                }
            })
        self.sec_column.show_scrollbar()
        self.first_column.show_scrollbar()

        self.sec_column.canvas.configure(scrollregion=self.sec_column.canvas.bbox("all"))
        self.first_column.canvas.configure(scrollregion=self.first_column.canvas.bbox("all"))


        self.main_button = tk.Button(
            self.button_frame,
            text="Enter data",
            command=self.on_main_submit
        )
        self.main_button.pack(side="top", fill='x')

        self.dynamic_widgets.extend([
            {'frame': properties_frame, 'type': 'properties', 'widgets': {
                'band_gap': self.entry_bg,
                'pce_percent': self.entry_pp,
                'voc': self.entry_voc,
                'jsc': self.entry_jsc,
                'ff_percent': self.entry_ff_percent,
                'stability_notes': self.entry_stability_notes
            }},
            {'frame': self.v_antisolvent_label, 'type': 'additional'},
            {'frame': self.v_antisolvent_entry, 'type': 'additional'},
            {'frame': self.tot_anion_s_label, 'type': 'additional'},
            {'frame': self.tot_anion_s_entry, 'type': 'additional'}
        ])

    def on_info_submit(self):
        name_phase = self.phase_template.get()
        id_template = analysis.get_template_id(name_phase)
        data = {
            'doi': self.entry_doi.get(),
            'data_type': self.data_box.get(),
            'notes': self.entry_notes.get(),
            'id_template': id_template,
            'num_elements': self.entry_num_elements.get(),
            'num_solvents': self.entry_num_solv.get(),
            'num_k': self.entry_k_fact.get()
        }
        self.controller.handle_info_submit(data)

    def on_main_submit(self):
        structure_data = []
        for widget in self.dynamic_widgets:
            if widget['type'] == 'structure':
                data = {
                    'structure_type': widget['widgets']['structure_type'].get(),
                    'symbol': widget['widgets']['symbol'].get(),
                    'fraction': widget['widgets']['fraction'].get(),
                    'valence': widget['widgets']['valence'].get()
                }
                structure_data.append(data)

        solvent_data = []
        for widget in self.dynamic_widgets:
            if widget['type'] == 'solvent':
                data = {
                    'solvent_type': widget['widgets']['solvent_type'].get(),
                    'symbol': widget['widgets']['symbol'].get(),
                    'fraction': widget['widgets']['fraction'].get()
                }
                solvent_data.append(data)

        factors_data = []
        for widget in self.dynamic_widgets:
            if widget['type'] == 'k_factors':
                data = {
                    'precursor': widget['widgets']['precursor'].get(),
                    'k_factor': widget['widgets']['k_factor'].get()
                }
                factors_data.append(data)

        properties_data = {
            'band_gap': self.entry_bg.get(),
            'ff_percent': self.entry_ff_percent.get(),
            'pce_percent': self.entry_pp.get(),
            'voc': self.entry_voc.get(),
            'jsc': self.entry_jsc.get(),
            'stability_notes': self.entry_stability_notes.get(),
            'v_antisolvent': self.v_antisolvent_entry.get(),
            'v_solution': self.v_antisolvent_entry.get(),
            'c_solution': self.c_solution_entry.get(),
            'anion_stoichiometry': self.tot_anion_s_entry.get(),
            'method_description': self.method_description_entry.get()
        }

        self.controller.handle_main_submit(structure_data, solvent_data, properties_data, factors_data)

    def show_success(self, message):
        tk.messagebox.showinfo(title="success", message=message)
        self.clear_form()

    def show_error(self, message):
        tk.messagebox.showerror(title="error", message=message)

    def clear_form(self):
        self.entry_doi.delete(0, tk.END)
        self.data_box.set('')
        self.entry_notes.delete(0, tk.END)
        self.entry_num_elements.delete(0, tk.END)
        self.phase_template.set('')
        self.entry_num_solv.delete(0, tk.END)
        self.entry_k_fact.delete(0, tk.END)

        for widget in self.dynamic_widgets:
            if 'widgets' in widget:
                for entry in widget['widgets'].values():
                    if isinstance(entry, tk.Entry):
                        entry.delete(0, tk.END)
                    elif isinstance(entry, ttk.Combobox):
                        entry.set('')

        self.v_antisolvent_entry.delete(0, tk.END)
        self.tot_anion_s_entry.delete(0, tk.END)