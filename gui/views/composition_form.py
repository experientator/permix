import tkinter as tk
from tkinter import ttk
from analysis import get_templates_list


class CompositionView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Add new composition")
        self.build_ui()
        self.dynamic_widgets = []

    def build_ui(self):
        self.container = tk.Frame(self, padx=20, pady=20)
        self.container.pack(expand=True, fill='both')

        self.first_column = ttk.Frame(self.container)
        self.sec_column = ttk.Frame(self.container)
        self.third_column = ttk.Frame(self.container)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill='x', pady=10)

        self.first_column.pack(side='left', fill='both', expand=True, padx=5)
        self.sec_column.pack(side='left', fill='both', expand=True, padx=5)
        self.third_column.pack(side='left', fill='both', expand=True, padx=5)

        self.create_info_frame()
        self.first_button = tk.Button(
            self.first_column,
            text="Enter info",
            command=self.on_info_submit
        )
        self.first_button.pack(fill='x', pady=5)

    def create_info_frame(self):
        info_frame = tk.LabelFrame(self.first_column, text="Composition information")
        info_frame.pack(fill='x', pady=5)

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

    def create_dynamic_widgets(self, num_elements, num_solvents):

        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets = []

        for i in range(num_elements):
            frame = tk.LabelFrame(self.sec_column, text=f"Element {i + 1}")
            frame.pack(fill='x', pady=5)

            tk.Label(frame, text="structure type").grid(row=0, column=0)
            structure_box = ttk.Combobox(frame, values=["A_site", "B_site", "B_double", "spacer_site", "anion"])
            structure_box.grid(row=1, column=0)

            tk.Label(frame, text="symbol").grid(row=0, column=1)
            entry_symbol = tk.Entry(frame)
            entry_symbol.grid(row=1, column=1)

            tk.Label(frame, text="fraction").grid(row=0, column=2)
            entry_fraction = tk.Entry(frame)
            entry_fraction.grid(row=1, column=2)

            tk.Label(frame, text="valence").grid(row=0, column=3)
            entry_valence = tk.Entry(frame)
            entry_valence.grid(row=1, column=3)

            self.dynamic_widgets.append({
                'frame': frame,
                'type': 'structure',
                'widgets': {
                    'structure_type': structure_box,
                    'symbol': entry_symbol,
                    'fraction': entry_fraction,
                    'valence': entry_valence
                }
            })

        for i in range(num_solvents):
            frame = tk.LabelFrame(self.third_column, text=f"Solvent {i + 1}")
            frame.pack(fill='x', pady=5)

            tk.Label(frame, text="type").grid(row=0, column=0)
            type_box = ttk.Combobox(frame, values=["solvent", "antisolvent"])
            type_box.grid(row=1, column=0)

            tk.Label(frame, text="symbol").grid(row=0, column=1)
            entry_symbol = tk.Entry(frame)
            entry_symbol.grid(row=1, column=1)

            tk.Label(frame, text="fraction").grid(row=0, column=2)
            entry_fraction = tk.Entry(frame)
            entry_fraction.grid(row=1, column=2)

            self.dynamic_widgets.append({
                'frame': frame,
                'type': 'solvent',
                'widgets': {
                    'solvent_type': type_box,
                    'symbol': entry_symbol,
                    'fraction': entry_fraction
                }
            })

        self.v_antisolvent_label = tk.Label(self.third_column, text="V antisolvent")
        self.v_antisolvent_label.pack(fill='x', pady=5)
        self.v_antisolvent_entry = tk.Entry(self.third_column)
        self.v_antisolvent_entry.pack(fill='x', pady=5)

        self.tot_anion_s_label = tk.Label(self.sec_column, text="total anion stoichiometry")
        self.tot_anion_s_label.pack(fill='x', pady=5)
        self.tot_anion_s_entry = tk.Entry(self.sec_column)
        self.tot_anion_s_entry.pack(fill='x', pady=5)

        properties_frame = tk.LabelFrame(self.first_column, text="Properties")
        properties_frame.pack(fill='x', pady=5)

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

        self.main_button = tk.Button(
            self.button_frame,
            text="Enter data",
            command=self.on_main_submit
        )
        self.main_button.pack(fill='x', pady=5)

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
        data = {
            'doi': self.entry_doi.get(),
            'data_type': self.data_box.get(),
            'notes': self.entry_notes.get(),
            'phase_template': self.phase_template.get(),
            'num_elements': self.entry_num_elements.get(),
            'num_solvents': self.entry_num_solv.get()
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

        properties_data = {
            'band_gap': self.entry_bg.get(),
            'ff_percent': self.entry_ff_percent.get(),
            'pce_percent': self.entry_pp.get(),
            'voc': self.entry_voc.get(),
            'jsc': self.entry_jsc.get(),
            'stability_notes': self.entry_stability_notes.get(),
            'v_antisolvent': self.v_antisolvent_entry.get(),
            'anion_stoichiometry': self.tot_anion_s_entry.get()
        }

        self.controller.handle_main_submit(structure_data, solvent_data, properties_data)

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

        for widget in self.dynamic_widgets:
            if 'widgets' in widget:
                for entry in widget['widgets'].values():
                    if isinstance(entry, tk.Entry):
                        entry.delete(0, tk.END)
                    elif isinstance(entry, ttk.Combobox):
                        entry.set('')

        self.v_antisolvent_entry.delete(0, tk.END)
        self.tot_anion_s_entry.delete(0, tk.END)