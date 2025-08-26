import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk, scrolledtext

from analysis.database_utils import (get_templates_list, get_template_id, get_template_sites,
                                     get_candidate_cations, get_solvents, get_anion_stoichiometry)
from analysis.chemistry_utils import get_salt_formula, calculate_target_anion_moles
from gui.controllers.templates_check import TemplatesCheckController
from analysis.masses_calculator import calculate_precursor_masses
from analysis.display_formatters import format_results_mass_table, generate_reaction_equations_display
from gui.default_style import AppStyles

class UserConfigView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.build_ui()
        self.create_template_frame()
        self.dynamic_widgets = []

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fraction_test(self, data, list, type_name):
        for element in data:
            try:
                fraction = float(element['fraction'])
            except ValueError:
                self.show_error(title = "error", message = "Fraction must be a float number")
                return

            if type_name == 'anion':
                list['anions'] += fraction
            else:
                type = element[f'{type_name}']
                list[type] += fraction

        for type, total in list.items():
            if total > 0 and not 0.99 <= total <= 1.01:
                self.show_error(title = "error", message =f"Total fraction for {type} must be 1")
                return

    def build_ui(self):
        # self.container = tk.Frame(self, **AppStyles.frame_style())
        # self.container.pack(expand=True, fill='both')

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.canvas, command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, **AppStyles.frame_style())
        self.canvas.create_window((0, 0), window=self.scrollable_frame)

        self.first_column = tk.Frame(self.scrollable_frame, **AppStyles.frame_style())
        self.first_column.pack(side="left", fill="both", expand=True, padx=10)

        self.sec_column = tk.Frame(self.scrollable_frame, **AppStyles.frame_style())
        self.sec_column.pack(side="left", fill="both", expand=True, padx=10)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # self.first_column.pack(side='left', fill='both', expand=True, padx=5)
        # self.sec_column.pack(side='right', fill='both', expand=True, padx=5)


    def open_template_form(self):
        TemplatesCheckController(self)

    def create_template_frame(self):
        info_frame = tk.LabelFrame(self.first_column,
                                   text="Выбор шаблона", **AppStyles.labelframe_style())
        info_frame.pack(fill='x', pady=5)
        self.results_frame = tk.LabelFrame(self.sec_column,
                                           text="Результаты расчетов", **AppStyles.labelframe_style())
        self.results_frame.pack(fill='x', pady=5)

        tk.Label(info_frame, text="Шаблон фазы",
                 **AppStyles.label_style()).pack(fill='x', pady=5)
        self.phase_template = ttk.Combobox(info_frame, values=get_templates_list(),
                                           **AppStyles.combobox_config())
        self.phase_template.current(0)
        self.phase_template.pack(fill='x', pady=5)

        tk.Button(info_frame, text="Просмотр шаблонов",
                 **AppStyles.button_style(),
                  command = self.open_template_form).pack(side="right", pady = 5, fill = 'x')
        self.button_entry = tk.Button(info_frame, text="Подтвердить",
                 **AppStyles.button_style(), command=self.create_sites)
        self.button_entry.pack(side="left", pady = 5, fill = 'x')

    def create_sites(self):
        self.button_entry["state"] = "disabled"
        self.sites_frame = tk.LabelFrame(self.first_column, text="Структура",
                 **AppStyles.labelframe_style())
        self.sites_frame.pack(fill='x', pady=5)

        self.name = self.phase_template.get()
        self.template_id = get_template_id(self.name)
        sites_data = get_template_sites(self.template_id)
        self.anion_stoichiometry = get_anion_stoichiometry(self.template_id)
        values_sites = ["1", "2", "3", "4"]

        for field in self.sites_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        tk.Label(self.sites_frame, text="Тип сайта",
                 **AppStyles.label_style()).grid(row=0, column=0)
        tk.Label(self.sites_frame, text="Кол-во",
                 **AppStyles.label_style()).grid(row=0, column=1)
        tk.Label(self.sites_frame, text="Катион",
                 **AppStyles.label_style()).grid(row=0, column=2)
        tk.Label(self.sites_frame, text="Доля",
                 **AppStyles.label_style()).grid(row=0, column=3)

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

            label_site = tk.Label(self.sites_frame, text=site_type,
                 **AppStyles.label_style())
            label_site.grid(row=current_row, column=0, padx=5, pady=2)
            combobox_num = ttk.Combobox(
                self.sites_frame,
                values=values_sites,
                state="readonly",
                width=5,
                ** AppStyles.combobox_config()
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
        label_site = tk.Label(self.sites_frame, text=site_type,
                 **AppStyles.label_style())
        label_site.grid(row=current_row, column=0, padx=5, pady=2)
        combobox_num = ttk.Combobox(
            self.sites_frame,
            values=values_sites,
            state="readonly",
            width=5,
            ** AppStyles.combobox_config()
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
        self.antisolv_check = tk.IntVar(self)
        self.anticolvents_cb = tk.Checkbutton(self.first_column, text = "Наличие антирастворителей",
                                               variable = self.antisolv_check, **AppStyles.checkbutton_style())
        self.anticolvents_cb.pack(fill='x', pady=5)
        self.upload_button = tk.Button(self.first_column, text = "подтвердить состав",
                 **AppStyles.button_style(), command = self.create_solvents)
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
                , **AppStyles.combobox_config()
            )
            if symbols:
                cb_symbol.current(0)
            cb_symbol.grid(row=row_pos, column=2, padx=5, pady=2)

            entry_fraction = tk.Entry(self.sites_frame, width=10, **AppStyles.entry_style())
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
        self.anticolvents_cb["state"] = "disabled"
        self.solvents_frame = tk.LabelFrame(self.first_column, text="растворители",
                                            **AppStyles.labelframe_style())
        self.solvents_frame.pack(fill='x', pady=5)

        if self.antisolv_check.get() == 1:
            self.solvent_types = ["solvent", "antisolvent"]
        else: self.solvent_types = ["solvent"]

        values_solvents = ["1", "2"]

        for field in self.solvents_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        tk.Label(self.solvents_frame, text="Тип растворителя",
                 **AppStyles.label_style()).grid(row=0, column=0)
        tk.Label(self.solvents_frame, text="Кол-во",
                 **AppStyles.label_style()).grid(row=0, column=1)
        tk.Label(self.solvents_frame, text="Катион",
                 **AppStyles.label_style()).grid(row=0, column=2)
        tk.Label(self.solvents_frame, text="Доля",
                 **AppStyles.label_style()).grid(row=0, column=3)

        self.solvents_widgets = {}

        for type in self.solvent_types:
            current_row = self.get_next_row(self.solvents_widgets)
            label_solvent = tk.Label(self.solvents_frame, text=type,
                 **AppStyles.label_style())
            label_solvent.grid(row=current_row, column=0, padx=5, pady=2)
            combobox_num = ttk.Combobox(
                self.solvents_frame,
                values=values_solvents,
                state="readonly",
                width=5,
                **AppStyles.combobox_config()
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
        self.target_anion_moles_map = calculate_target_anion_moles(anions, self.anion_stoichiometry)
        cation_valences = [cation["valence"] for cation in cations]
        cation_symbols = [cation["symbol"] for cation in cations]
        anion_symbols = [anion["symbol"] for anion in anions]
        for i in range(len(cation_symbols)):
            for anion_symbol in anion_symbols:
                self.salt_formulas.append(get_salt_formula(cation_symbols[i], anion_symbol, cation_valences[i]))
        value_salts = list(range(1, len(self.salt_formulas) + 1))
        self.current_row = 1
        self.k_factors_frame = tk.LabelFrame(self.first_column, text="K-факторы",
                                             **AppStyles.labelframe_style())
        self.k_factors_frame.pack(fill='x', pady=5)
        tk.Button(self.k_factors_frame, text="Просмотр возможных солей",
                  command = self.show_salts_info,
                 **AppStyles.button_style()).grid(row=0, column=0)
        tk.Button(self.k_factors_frame, text="Добавить k-фактор",
                  command = self.create_k_factors_widgets,
                 **AppStyles.button_style()).grid(row=0, column=1)
        tk.Label(self.k_factors_frame, text="Соль",
                 **AppStyles.label_style()).grid(row=1, column=0)
        tk.Label(self.k_factors_frame, text="К-фактор",
                 **AppStyles.label_style()).grid(row=1, column=1)
        self.k_factors_widgets = {}
        self.k_factors_widgets = {
            "dynamic_widgets": []
        }
        self.data_button()

    def data_button(self):
        self.data_apply_button_frame = tk.LabelFrame(self.first_column,
                                                     **AppStyles.labelframe_style())
        self.data_apply_button_frame.pack(fill='x')
        self.data_apply_button = tk.Button(self.data_apply_button_frame, text = "Начать расчет",
                                           command = self.calculations_function,
                                           ** AppStyles.button_style())
        self.data_apply_button.pack(fill='x')

    def calculations_function(self):
        self.cations_data, self.anions_data = self.get_structure_data()
        self.solvents_data, self.solution_info = self.get_solution_data()
        self.k_factors = self.get_k_factors_data()

        for element in self.k_factors:
            try:
                k_factor = float(element['k_factor'])
            except ValueError:
                self.show_error(title="error", message="k-факторы должны принимать числовые значения")
                return

        calculations = calculate_precursor_masses(
                self.template_id, self.cations_data,
                self.anions_data, self.anion_stoichiometry,
                self.solution_info, self.solvents_data,
                self.k_factors)
        self.console_text = scrolledtext.ScrolledText(
            self.results_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="black",
            fg="white",
            insertbackground="white"
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.console_text.config(state=tk.DISABLED)

        clear_btn = tk.Button(self.results_frame, text="Очистить",
                              command=self.clear_console, **AppStyles.button_style())
        clear_btn.pack(pady=5)

        self.fav_button = tk.Button(self.first_column, text="Сохранить конфигурацию",
                                    command=self.save_config, **AppStyles.button_style())
        self.fav_button.pack(pady=5)
        solvent_fractions = {'solvent': 0, 'antisolvent': 0}
        self.fraction_test(self.solvents_data, solvent_fractions, 'solvent_type')
        cation_fractions = {'a_site': 0, 'b_site': 0, 'b_double': 0, 'spacer': 0}
        self.fraction_test(self.cations_data, cation_fractions, 'structure_type')
        anions_fractions = {'anions': 0}
        self.fraction_test(self.anions_data, anions_fractions, 'anion')

        self.add_text(generate_reaction_equations_display(calculations))
        self.add_text(format_results_mass_table(calculations))

    def save_config(self):
        self.top_window = tk.Toplevel(self)
        self.top_window.title("Ввод данных")
        self.top_window.geometry("300x300")  # Размер окна

        tk.Label(self.top_window, text="Название конфигурации",
                 **AppStyles.label_style()).pack(pady=10)

        self.input_name = tk.Entry(self.top_window, width=30, **AppStyles.entry_style())
        self.input_name.pack(pady=5)

        tk.Label(self.top_window, text="Описание конфигурации",
                 **AppStyles.label_style()).pack(pady=10)

        self.input_notes = tk.Entry(self.top_window, width=30, **AppStyles.entry_style())
        self.input_notes.pack(pady=5)

        submit_button = tk.Button(self.top_window, text="Подтвердить",
                                  command=self.get_and_close, **AppStyles.button_style())
        submit_button.pack(pady=10)

    def get_and_close(self):
        self.name_fav = self.input_name.get()
        self.notes_fav = self.input_notes.get()
        self.controller.handle_main_submit(self.name_fav, self.notes_fav, self.solvents_data,
                                           self.cations_data, self.anions_data, self.k_factors,
                                           self.solution_info, self.template_id)
        self.top_window.destroy()

    def add_text(self, text):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, text)
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)

    def clear_console(self):
        self.console_text.destroy()

    def show_salts_info(self):
        salt_text = ""
        for salt in self.salt_formulas:
            salt_text += salt
            salt_text += ", "
        salt_text = salt_text[:-2]
        mb.showinfo("Список солей", f"Список возможных солей для данного соединения:{salt_text}")

    def create_k_factors_widgets(self):
        self.current_row+=1
        combobox_salts = ttk.Combobox(
            self.k_factors_frame,
            values=self.salt_formulas,
            state="readonly",
            width=5,
            **AppStyles.combobox_config()
        )
        combobox_salts.current(0)
        combobox_salts.grid(row=self.current_row, column=0, padx=5, pady=2)
        entry_k_factor = tk.Entry(self.k_factors_frame, width=10,
                                  **AppStyles.entry_style())
        entry_k_factor.grid(row=self.current_row, column=1, padx=5, pady=2)
        self.k_factors_widgets["dynamic_widgets"].append({
            "salt": combobox_salts,
            "k_factor": entry_k_factor
        })

    def get_solution_data(self):
        solvents = []
        for idx, solvent_type in enumerate(self.solvent_types):
            num_solvents = int(self.solvents_widgets[solvent_type]["combobox_num"].get())
            for i in range(num_solvents):
                widget = self.solvents_widgets[solvent_type]["dynamic_widgets"][i]
                solvents.append({
                    "solvent_type": solvent_type,
                    "symbol": widget["symbol"].get(),
                    "fraction": widget["fraction"].get(),
                })
        try:
            v_solvent = float(self.entry_v_solvent.get())
            c_solvent = float(self.entry_c_solvent.get())
            if self.antisolv_check == 1:
                v_antisolvent = float(self.entry_v_antisolvent.get())
        except ValueError:
            self.show_error(title="error", message="Характеристики раствора должны принимать численные значения")
            return

        solution_info = {
            "v_solvent": v_solvent,
            "c_solvent": c_solvent,
            "v_antisolvent": 0.0
        }
        if self.antisolv_check.get() == 1:
            solution_info["v_antisolvent"] = float(self.entry_v_antisolvent.get())
        return solvents, solution_info

    def get_k_factors_data(self):
        k_factors = []
        num_k_factors = len(self.k_factors_widgets["dynamic_widgets"])
        for i in range(num_k_factors):
            widget = self.k_factors_widgets["dynamic_widgets"][i]
            k_factors.append({
                "salt": widget["salt"].get(),
                "k_factor": widget["k_factor"].get(),
            })
        return k_factors

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
                    "stoichiometry": float(stoichiometry),
                    "real_stoichiometry": float(stoichiometry)*float(widget["fraction"].get())
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
                state="readonly",
                ** AppStyles.combobox_config()
            )
            if symbols:
                cb_symbol.current(0)
            cb_symbol.grid(row=row_pos, column=2, padx=5, pady=2)

            entry_fraction = tk.Entry(self.solvents_frame, width=10, **AppStyles.entry_style())
            entry_fraction.grid(row=row_pos, column=3, padx=5, pady=2)
            self.solvents_widgets[solvent_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.solvents_widgets)

    def create_solvent_properties(self):
        self.propereties_frame = tk.LabelFrame(self.first_column, text="свойства раствора",
                                               **AppStyles.labelframe_style())
        self.propereties_frame.pack(fill='x', pady=5)
        tk.Label(self.propereties_frame, text="Объем раствора",
                 **AppStyles.label_style()).grid(row=0, column=0)
        tk.Label(self.propereties_frame, text="Концентрация раствора",
                 **AppStyles.label_style()).grid(row=0, column=1)
        if self.antisolv_check.get() == 1:
            tk.Label(self.propereties_frame, text="Объем антирастворителя",
                 **AppStyles.label_style()).grid(row=0, column=2)

        self.entry_v_solvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
        self.entry_v_solvent.grid(row=1, column=0)
        self.entry_c_solvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
        self.entry_c_solvent.grid(row=1, column=1)
        if self.antisolv_check.get() == 1:
            self.entry_v_antisolvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
            self.entry_v_antisolvent.grid(row=1, column=2)

    def show_error(self, title, message):
        tk.messagebox.showerror(title, message)
