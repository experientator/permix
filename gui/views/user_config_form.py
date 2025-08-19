import tkinter as tk
from tkinter import ttk

from analysis.database_utils import (get_templates_list, get_template_id, get_template_sites,
                                     get_candidate_cations, get_solvents, get_anion_stoichiometry)
from analysis.chemistry_utils import get_salt_formula, calculate_target_anion_moles
from analysis.strategies import calculate_coefficients_all_flexible
from gui.controllers.templates_check import TemplatesCheckController

class UserConfigView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Main calculator")
        self.build_ui()
        self.create_template_frame()
        self.dynamic_widgets = []

    def build_ui(self):
        self.container = tk.Frame(self, padx=20, pady=20)
        self.container.pack(expand=True, fill='both')

        self.first_column = ttk.Frame(self.container)
        self.sec_column = ttk.Frame(self.container)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill='x', pady=10)

        self.first_column.pack(side='left', fill='both', expand=True, padx=5)
        self.sec_column.pack(side='left', fill='both', expand=True, padx=5)

    def open_template_form(self):
        TemplatesCheckController(self)

    def create_template_frame(self):
        info_frame = tk.LabelFrame(self.first_column, text="Выбор шаблона")
        info_frame.pack(fill='x', pady=5)

        tk.Label(info_frame, text="Шаблон фазы").pack(fill='x', pady=5)
        self.phase_template = ttk.Combobox(info_frame, values=get_templates_list())
        self.phase_template.pack(fill='x', pady=5)

        tk.Button(info_frame, text="Просмотр шаблонов", command = self.open_template_form).pack(side="right", pady = 5)
        self.button_entry = tk.Button(info_frame, text="Подтвердить", command=self.create_sites)
        self.button_entry.pack(side="left", pady = 5)

    def create_sites(self):
        self.button_entry["state"] = "disabled"
        self.sites_frame = tk.LabelFrame(self.first_column, text="Структура")
        self.sites_frame.pack(fill='x', pady=5)

        self.name = self.phase_template.get()
        template_id = get_template_id(self.name)
        sites_data = get_template_sites(template_id)
        self.anion_stoichiometry = get_anion_stoichiometry(template_id)
        values_sites = ["1", "2", "3", "4"]

        for field in self.sites_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        tk.Label(self.sites_frame, text="Тип сайта").grid(row=0, column=0)
        tk.Label(self.sites_frame, text="Кол-во").grid(row=0, column=1)
        tk.Label(self.sites_frame, text="Катион").grid(row=0, column=2)
        tk.Label(self.sites_frame, text="Доля").grid(row=0, column=3)

        self.site_widgets = {}
        self.structure_types = []
        self.structure_valences = []
        self.structure_stoichiometry = []
        for index, sites_row in sites_data.iterrows():
            site_type = sites_row["type"]
            self.structure_types.append(site_type)
            self.structure_valences.append(sites_row["valence"])
            self.structure_stoichiometry.append(sites_row["stoichiometry"])
            site_candidate = sites_row["name_candidate"]
            current_row = self.get_next_row(self.site_widgets)

            label_site = tk.Label(self.sites_frame, text=site_type)
            label_site.grid(row=current_row, column=0, padx=5, pady=2)
            combobox_num = ttk.Combobox(
                self.sites_frame,
                values=values_sites,
                state="readonly",
                width=5
            )
            combobox_num.current(0)
            combobox_num.grid(row=current_row, column=1, padx=5, pady=2)
            combobox_num.bind(
                "<<ComboboxSelected>>",
                lambda e, st=site_type, sc=site_candidate: self._update_site(st, sc)
            )

            self.site_widgets[site_type] = {
                "label": label_site,
                "combobox_num": combobox_num,
                "dynamic_widgets": []
            }
            self._update_site(site_type, site_candidate)

        current_row = self.get_next_row(self.site_widgets)
        site_type = "anion"
        label_site = tk.Label(self.sites_frame, text=site_type)
        label_site.grid(row=current_row, column=0, padx=5, pady=2)
        combobox_num = ttk.Combobox(
            self.sites_frame,
            values=values_sites,
            state="readonly",
            width=5
        )
        combobox_num.current(0)
        combobox_num.grid(row=current_row, column=1, padx=5, pady=2)
        combobox_num.bind(
            "<<ComboboxSelected>>",
            lambda e, st=site_type, sc=0: self._update_site(st, sc)
        )
        self.site_widgets[site_type] = {
            "label": label_site,
            "combobox_num": combobox_num,
            "dynamic_widgets": []
        }
        self._update_site(site_type, 0)

        self.upload_button = tk.Button(self.first_column, text = "подтвердить состав", command = self.create_solvents)
        self.upload_button.pack(fill='x', pady=5)

    def get_next_row(self, widget):
        if not widget:
            return 1

        last_row = 0
        for data in widget.values():
            last_row = max(last_row, data["label"].grid_info()["row"])
            for field in data["dynamic_widgets"]:
                last_row = max(last_row, field["symbol"].grid_info()["row"])
                last_row = max(last_row, field["fraction"].grid_info()["row"])
        return last_row + 1

    def _update_site(self, site_type, site_candidate):
        for field in self.site_widgets[site_type]["dynamic_widgets"]:
            field["symbol"].destroy()
            field["fraction"].destroy()
        self.site_widgets[site_type]["dynamic_widgets"] = []
        num_sites = int(self.site_widgets[site_type]["combobox_num"].get())
        if site_type == "anion":
            symbols = ["Cl", "Br", "I"]
        else:
            symbols = get_candidate_cations(site_candidate)
        start_row = self.site_widgets[site_type]["label"].grid_info()["row"] + 1

        for i in range(num_sites):
            row_pos = start_row + i

            cb_symbol = ttk.Combobox(
                self.sites_frame,
                values=symbols,
                state="readonly"
            )
            if symbols:
                cb_symbol.current(0)
            cb_symbol.grid(row=row_pos, column=2, padx=5, pady=2)

            entry_fraction = tk.Entry(self.sites_frame, width=10)
            entry_fraction.grid(row=row_pos, column=3, padx=5, pady=2)
            self.site_widgets[site_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.site_widgets)

    def recalculate_all_positions(self, widget):
        current_row = 1

        for site_type in widget:
            widget[site_type]["label"].grid(row=current_row, column=0)
            widget[site_type]["combobox_num"].grid(row=current_row, column=1)

            for field in widget[site_type]["dynamic_widgets"]:
                field["symbol"].grid(row=current_row, column=2)
                field["fraction"].grid(row=current_row, column=3)
                current_row += 1

    def create_solvents(self):
        self.upload_button["state"] = "disabled"
        self.solvents_frame = tk.LabelFrame(self.first_column, text="растворители")
        self.solvents_frame.pack(fill='x', pady=5)

        solvent_type = ["solvent", "antisolvent"]
        values_solvents = ["1", "2"]

        for field in self.solvents_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        tk.Label(self.solvents_frame, text="Тип растворителя").grid(row=0, column=0)
        tk.Label(self.solvents_frame, text="Кол-во").grid(row=0, column=1)
        tk.Label(self.solvents_frame, text="Катион").grid(row=0, column=2)
        tk.Label(self.solvents_frame, text="Доля").grid(row=0, column=3)

        self.solvents_widgets = {}

        for type in solvent_type:
            current_row = self.get_next_row(self.solvents_widgets)
            label_solvent = tk.Label(self.solvents_frame, text=type)
            label_solvent.grid(row=current_row, column=0, padx=5, pady=2)
            combobox_num = ttk.Combobox(
                self.solvents_frame,
                values=values_solvents,
                state="readonly",
                width=5
            )
            combobox_num.current(0)
            combobox_num.grid(row=current_row, column=1, padx=5, pady=2)
            combobox_num.bind(
                "<<ComboboxSelected>>",
                lambda e, t = type: self._update_solvent(t)
            )

            self.solvents_widgets[type] = {
                "label": label_solvent,
                "combobox_num": combobox_num,
                "dynamic_widgets": []
            }

            self._update_solvent(type)
        self.create_solvent_properties()
        self.create_k_factors_frame()

    def create_k_factors_frame(self):
        self.salt_formulas = []
        cations, anions = self.get_structure_data()
        anions_listt = calculate_target_anion_moles(anions, self.anion_stoichiometry)
        print(calculate_coefficients_all_flexible(cations, anions_listt))
        cation_valences = [cation["valence"] for cation in cations]
        cation_symbols = [cation["symbol"] for cation in cations]
        anion_symbols = [anion["symbol"] for anion in anions]
        for i in range(len(cation_symbols)):
            for anion_symbol in anion_symbols:
                self.salt_formulas.append(get_salt_formula(cation_symbols[i], anion_symbol, cation_valences[i]))
        value_salts = list(range(1, len(self.salt_formulas) + 1))
        self.current_row = 1
        self.k_factors_frame = tk.LabelFrame(self.first_column, text="K-факторы")
        self.k_factors_frame.pack(fill='x', pady=5)
        tk.Button(self.k_factors_frame, text="Просмотр возможных солей",
                  command = self.create_k_factors_widgets).grid(row=0, column=0)
        tk.Button(self.k_factors_frame, text="Добавить k-фактор",
                  command = self.create_k_factors_widgets).grid(row=0, column=1)
        tk.Label(self.k_factors_frame, text="Соль").grid(row=1, column=0)
        tk.Label(self.k_factors_frame, text="К-фактор").grid(row=1, column=1)
        self.k_factors_widgets = {}

    def create_k_factors_widgets(self):
        self.current_row+=1
        combobox_salts = ttk.Combobox(
            self.k_factors_frame,
            values=self.salt_formulas,
            state="readonly",
            width=5
        )
        combobox_salts.current(0)
        combobox_salts.grid(row=self.current_row, column=0, padx=5, pady=2)
        entry_k_factor = tk.Entry(self.k_factors_frame, width=10)
        entry_k_factor.grid(row=self.current_row, column=1, padx=5, pady=2)

    def get_structure_data(self):
        cations = []
        anions = []
        for idx, site_type in enumerate(self.structure_types):
            num_sites = int(self.site_widgets[site_type]["combobox_num"].get())
            valence = self.structure_valences[idx]
            stoichiometry = self.structure_stoichiometry[idx]

            for i in range(num_sites):
                widget = self.site_widgets[site_type]["dynamic_widgets"][i]
                cations.append({
                    "structure_type": site_type,
                    "symbol": widget["symbol"].get(),
                    "fraction": widget["fraction"].get(),
                    "valence": valence,
                    "real_stoichiometry": float(stoichiometry)*float(valence)
                })

        num_anions = int(self.site_widgets["anion"]["combobox_num"].get())
        for i in range(num_anions):
            widget = self.site_widgets["anion"]["dynamic_widgets"][i]
            anions.append({
                "symbol": widget["symbol"].get(),
                "fraction": widget["fraction"].get(),
            })
        return cations, anions

    def _update_solvent(self, solvent_type):
        for field in self.solvents_widgets[solvent_type]["dynamic_widgets"]:
            field["symbol"].destroy()
            field["fraction"].destroy()
        self.solvents_widgets[solvent_type]["dynamic_widgets"] = []
        num_solvents = int(self.solvents_widgets[solvent_type]["combobox_num"].get())
        symbols = get_solvents(solvent_type)
        start_row = self.solvents_widgets[solvent_type]["label"].grid_info()["row"] + 1

        for i in range(num_solvents):
            row_pos = start_row + i

            cb_symbol = ttk.Combobox(
                self.solvents_frame,
                values=symbols,
                state="readonly"
            )
            if symbols:
                cb_symbol.current(0)
            cb_symbol.grid(row=row_pos, column=2, padx=5, pady=2)

            entry_fraction = tk.Entry(self.solvents_frame, width=10)
            entry_fraction.grid(row=row_pos, column=3, padx=5, pady=2)
            self.solvents_widgets[solvent_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.solvents_widgets)

    def create_solvent_properties(self):
        self.propereties_frame = tk.LabelFrame(self.first_column, text="свойства раствора")
        self.propereties_frame.pack(fill='x', pady=5)
        tk.Label(self.propereties_frame, text="Объем раствора").grid(row=0, column=0)
        tk.Label(self.propereties_frame, text="Концентрация раствора").grid(row=0, column=1)
        tk.Label(self.propereties_frame, text="Объем антирастворителя").grid(row=0, column=2)

        self.entry_v_solvent = tk.Entry(self.propereties_frame, width=10)
        self.entry_v_solvent.grid(row=1, column=0, padx=5, pady=2)
        self.entry_c_solvent = tk.Entry(self.propereties_frame, width=10)
        self.entry_c_solvent.grid(row=1, column=1, padx=5, pady=2)
        self.entry_v_antisolvent = tk.Entry(self.propereties_frame, width=10)
        self.entry_v_antisolvent.grid(row=1, column=2, padx=5, pady=2)