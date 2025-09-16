import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk, scrolledtext

from analysis.database_utils import (get_templates_list, get_template_id, get_template_sites,
                                     get_candidate_cations, get_solvents, get_anion_stoichiometry)
from analysis.chemistry_utils import get_salt_formula, calculate_target_anion_moles
from gui.controllers.templates_check import TemplatesCheckController
from analysis.masses_calculator import calculate_precursor_masses
from analysis.calculation_tests import fraction_test, float_test
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

    def build_ui(self):
        main_frame = tk.Frame(self, **AppStyles.frame_style())
        main_frame.pack(fill="both", expand=True)

        # Убираем общий скроллбар и канву
        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=5)

        # ПЕРВАЯ КОЛОНКА - со скроллом
        first_column_container = tk.Frame(self.paned_window, **AppStyles.frame_style())
        self.paned_window.add(first_column_container, weight=1)

        # Канва и скроллбар только для первой колонки
        canvas = tk.Canvas(first_column_container, borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(first_column_container, orient="vertical", command=canvas.yview)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        self.first_column = tk.Frame(canvas, **AppStyles.frame_style())
        canvas_window = canvas.create_window((0, 0), window=self.first_column, anchor="nw")

        # Привязка событий для первой колонки
        self.first_column.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # Привязка колесика мыши только к первой колонке
        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        self.first_column.bind("<Enter>", bind_mousewheel)
        self.first_column.bind("<Leave>", unbind_mousewheel)

        # ВТОРАЯ КОЛОНКА - без скролла
        self.sec_column = tk.Frame(self.paned_window, **AppStyles.frame_style())
        self.paned_window.add(self.sec_column, weight=3)

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
        self.phase_template = ttk.Combobox(info_frame,
                                           values=get_templates_list(),
                                           state="readonly",
                                           **AppStyles.combobox_config())
        self.phase_template.current(0)
        self.phase_template.pack(fill='x', pady=5)

        button_frame = tk.Frame(info_frame)
        button_frame.pack(fill='x', pady=5)

        tk.Button(button_frame, text="Просмотр шаблонов",
                  **AppStyles.button_style(),
                  command=self.open_template_form).pack(side="right", expand=True, fill = 'x', padx=2)

        self.button_entry = tk.Button(button_frame, text="Подтвердить",
                                      **AppStyles.button_style(), command=self.create_sites)
        self.button_entry.pack(side="right", expand=True, fill = 'x', padx=2)

        clear_btn = tk.Button(button_frame, text="Очистить форму",
                              **AppStyles.button_style(), command=self.reset_form)
        clear_btn.pack(side="right", expand=True, fill = 'x', padx=2)

    def create_sites(self):
        self.button_entry["state"] = "disabled"
        self.sites_frame = tk.LabelFrame(self.first_column, text="Структура",
                 **AppStyles.labelframe_style())
        self.sites_frame.pack(fill='both', pady=5, expand=True)

        self.name = self.phase_template.get()
        self.template_id = get_template_id(self.name)
        sites_data = get_template_sites(self.template_id)
        self.anion_stoichiometry = get_anion_stoichiometry(self.template_id)
        values_sites = ["1", "2", "3", "4"]

        for field in self.sites_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        self.sites_frame.columnconfigure(0, weight=1)
        self.sites_frame.columnconfigure(1, weight=1)
        self.sites_frame.columnconfigure(2, weight=2)
        self.sites_frame.columnconfigure(3, weight=2)

        tk.Label(self.sites_frame, text="Тип сайта",
                 **AppStyles.label_style()).grid(row=0, column=0, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.sites_frame, text="Кол-во",
                 **AppStyles.label_style()).grid(row=0, column=1, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.sites_frame, text="Катион",
                 **AppStyles.label_style()).grid(row=0, column=2, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.sites_frame, text="Доля",
                 **AppStyles.label_style()).grid(row=0, column=3, sticky = 'ew', padx=5, pady=2)

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
            label_site.grid(row=current_row, column=0, padx=5, pady=2, sticky = 'ew')
            combobox_num = ttk.Combobox(
                self.sites_frame,
                values=values_sites,
                state="readonly",
                width=5,
                ** AppStyles.combobox_config()
            )
            combobox_num.current(0)
            combobox_num.grid(row=current_row, column=1, padx=5, pady=2, sticky = 'ew')
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
        label_site.grid(row=current_row, column=0, padx=5, pady=2, sticky = 'ew')
        combobox_num = ttk.Combobox(
            self.sites_frame,
            values=values_sites,
            state="readonly",
            width=5,
            ** AppStyles.combobox_config()
        )
        combobox_num.current(0)
        combobox_num.grid(row=current_row, column=1, padx=5, pady=2, sticky = 'ew')
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
        self.antisolvents_cb = tk.Checkbutton(self.first_column, text = "Наличие антирастворителей",
                                               variable = self.antisolv_check, **AppStyles.checkbutton_style())
        self.antisolvents_cb.pack(fill='x', pady=5)
        self.upload_button = tk.Button(self.first_column, text = "подтвердить состав",
                 **AppStyles.button_style(), command = self.create_solvents)
        self.upload_button.pack(pady=5, expand=True, fill = 'x')

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
            cb_symbol.grid(row=row_pos, column=2, padx=5, pady=2, sticky = 'ew')

            entry_fraction = tk.Entry(self.sites_frame, width=10, **AppStyles.entry_style())
            entry_fraction.insert(0, "1")
            entry_fraction.grid(row=row_pos, column=3, padx=5, pady=2, sticky = 'ew')
            self.site_widgets[site_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.site_widgets)

    def recalculate_all_positions(self, widget):
        current_row = 1

        for site_type in widget:
            widget[site_type]["label"].grid(row=current_row, column=0, sticky = 'ew', padx=5, pady=2)
            widget[site_type]["combobox_num"].grid(row=current_row, column=1, sticky = 'ew', padx=5, pady=2)

            for field in widget[site_type]["dynamic_widgets"]:
                field["symbol"].grid(row=current_row, column=2, sticky = 'ew', padx=5, pady=2)
                field["fraction"].grid(row=current_row, column=3, sticky = 'ew', padx=5, pady=2)
                current_row += 1

    def create_solvents(self):
        self.salt_formulas = []
        self.cations_data, self.anions_data = self.get_structure_data()

        cation_fractions = {'a_site': 0, 'b_site': 0, 'b_double': 0, 'spacer': 0}
        anions_fractions = {'anions': 0}

        try:
            fraction_test(self.cations_data, cation_fractions, 'structure_type')
            fraction_test(self.anions_data, anions_fractions, 'anion')
        except (ValueError, TypeError):
            return

        self.target_anion_moles_map = calculate_target_anion_moles(self.anions_data, self.anion_stoichiometry)
        cation_valences = [cation["valence"] for cation in self.cations_data]
        cation_symbols = [cation["symbol"] for cation in self.cations_data]
        anion_symbols = [anion["symbol"] for anion in self.anions_data]
        for i in range(len(cation_symbols)):
            for anion_symbol in anion_symbols:
                self.salt_formulas.append(get_salt_formula(cation_symbols[i], anion_symbol, cation_valences[i]))

        self.upload_button["state"] = "disabled"
        self.antisolvents_cb["state"] = "disabled"
        self.solvents_frame = tk.LabelFrame(self.first_column, text="растворители",
                                            **AppStyles.labelframe_style())
        self.solvents_frame.pack(expand=True, fill = 'x', pady=5)
        self.solvents_frame.columnconfigure(0, weight=1)
        self.solvents_frame.columnconfigure(1, weight=1)
        if self.antisolv_check.get() == 1:
            self.solvent_types = ["solvent", "antisolvent"]
        else: self.solvent_types = ["solvent"]

        values_solvents = ["1", "2"]

        for field in self.solvents_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        tk.Label(self.solvents_frame, text="Тип растворителя",
                 **AppStyles.label_style()).grid(row=0, column=0, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.solvents_frame, text="Кол-во",
                 **AppStyles.label_style()).grid(row=0, column=1, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.solvents_frame, text="Название растворителя",
                 **AppStyles.label_style()).grid(row=0, column=2, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.solvents_frame, text="Доля",
                 **AppStyles.label_style()).grid(row=0, column=3, sticky = 'ew', padx=5, pady=2)

        self.solvents_widgets = {}

        for type in self.solvent_types:
            if type == "solvent":
                text_type = "Растворитель"
            else:
                text_type = "Антирастворитель"
            current_row = self.get_next_row(self.solvents_widgets)
            label_solvent = tk.Label(self.solvents_frame, text=text_type,
                 **AppStyles.label_style())
            label_solvent.grid(row=current_row, column=0, sticky = 'ew', padx=5, pady=2)
            combobox_num = ttk.Combobox(
                self.solvents_frame,
                values=values_solvents,
                state="readonly",
                width=5,
                **AppStyles.combobox_config()
            )
            combobox_num.current(0)
            combobox_num.grid(row=current_row, column=1, sticky = 'ew', padx=5, pady=2)
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
        self.data_button()

    def create_k_factors_frame(self):
        self.current_row = 1
        self.k_factors_frame = tk.LabelFrame(self.first_column, text="K-факторы",
                                             **AppStyles.labelframe_style())
        self.k_factors_frame.pack(expand=True, fill = 'x', pady=5)

        self.k_factors_frame.columnconfigure(0, weight=1)
        self.k_factors_frame.columnconfigure(1, weight=1)

        tk.Button(self.k_factors_frame, text="Просмотр возможных солей",
                  command=self.show_salts_info,
                  **AppStyles.button_style()).grid(row=0, column=0, sticky = 'ew', padx=5, pady=2)

        tk.Button(self.k_factors_frame, text="Добавить k-фактор",
                  command=self.create_k_factors_widgets,
                  **AppStyles.button_style()).grid(row=0, column=1, sticky = 'ew', padx=5, pady=2)


        tk.Label(self.k_factors_frame, text="Соль",
                 **AppStyles.label_style()).grid(row=1, column=0, sticky = 'ew', padx=5, pady=2)

        tk.Label(self.k_factors_frame, text="К-фактор",
                 **AppStyles.label_style()).grid(row=1, column=1, sticky = 'ew', padx=5, pady=2)

        self.k_factors_widgets = {
            "dynamic_widgets": []
        }


    def data_button(self):
        self.data_apply_button = tk.Button(self.first_column, text = "Начать расчет",
                                           command = self.calculations_function,
                                           ** AppStyles.button_style())
        self.data_apply_button.pack(expand=True, fill = 'x', pady=5)

    def calculations_function(self):
        self.k_factors = self.get_k_factors_data()
        self.solvents_data, self.solution_info = self.get_solution_data()
        solvent_fractions = {'solvent': 0, 'antisolvent': 0}
        fraction_test(self.solvents_data, solvent_fractions, 'solvent_type')

        for element in self.k_factors:
            k_factor = float_test(element['k_factor'], "К-факторы")

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

        self.fav_button = tk.Button(self.first_column, text="Сохранить конфигурацию",
                                    command=self.save_config, **AppStyles.button_style())
        self.fav_button.pack(expand=True, fill = 'x', pady=5)
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

    def show_salts_info(self):
        salt_text = ""
        for salt in self.salt_formulas:
            salt_text += salt
            salt_text += ", "
        salt_text = salt_text[:-2]
        mb.showinfo("Список солей", f"Список возможных солей для данного соединения:{salt_text}")

    def create_k_factors_widgets(self):

        self.current_row += 1

        combobox_salts = ttk.Combobox(
            self.k_factors_frame,
            values=self.salt_formulas,
            state="readonly",
            width=5,
            **AppStyles.combobox_config()
        )
        combobox_salts.current(0)
        combobox_salts.grid(row=self.current_row, column=0, sticky = 'ew', padx=5, pady=2)
        entry_k_factor = tk.Entry(self.k_factors_frame, width=10,
                                  **AppStyles.entry_style())
        entry_k_factor.grid(row=self.current_row, column=1, sticky = 'ew', padx=5, pady=2)
        self.k_factors_widgets["dynamic_widgets"].append({
            "salt": combobox_salts,
            "k_factor": entry_k_factor
        })

    def get_solution_data(self):
        used_symbols = set()
        solvents = []
        for idx, solvent_type in enumerate(self.solvent_types):
            num_solvents = int(self.solvents_widgets[solvent_type]["combobox_num"].get())
            for i in range(num_solvents):
                widget = self.solvents_widgets[solvent_type]["dynamic_widgets"][i]

                symbol = widget["symbol"].get()

                if symbol in used_symbols:
                    self.show_error("Ошибка", f"Растворитель '{symbol}' повторяется")
                    return None, None
                used_symbols.add(symbol)

                solvents.append({
                    "solvent_type": solvent_type,
                    "symbol": widget["symbol"].get(),
                    "fraction": widget["fraction"].get(),
                })
        try:
            v_solvent = float(self.entry_v_solvent.get())
            c_solvent = float(self.entry_c_solvent.get())
            if self.antisolv_check.get() == 1:
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
        used_salts = set()
        k_factors = []
        num_k_factors = len(self.k_factors_widgets["dynamic_widgets"])
        for i in range(num_k_factors):
            widget = self.k_factors_widgets["dynamic_widgets"][i]

            symbol = widget["salt"].get()

            if symbol in used_salts:
                self.show_error("Ошибка", f"Соль '{symbol}' повторяется")
                return None, None
            used_salts.add(symbol)
            k_factor = float_test(widget["k_factor"].get(), "К-факторы")
            k_factors.append({
                "salt": widget["salt"].get(),
                "k_factor": k_factor,
            })
        return k_factors

    def get_structure_data(self):
        used_symbols = set()
        cations = []
        anions = []
        for idx, site_type in enumerate(self.structure_types):
            num_sites = int(self.site_widgets[site_type]["combobox_num"].get())
            valence = self.structure_valences[idx]
            stoichiometry = self.structure_stoichiometry[idx]
            for i in range(num_sites):
                widget = self.site_widgets[site_type]["dynamic_widgets"][i]
                fraction = float_test(widget["fraction"].get(), "Доли")
                if fraction is None:
                    return None, None
                symbol = widget["symbol"].get()
                if symbol in used_symbols:
                    self.show_error("Ошибка", f"Катион '{symbol}' повторяется")
                    widget["symbol"].configure(background="#ffcccc")
                    return None, None
                used_symbols.add(symbol)
                cations.append({
                    "structure_type": site_type,
                    "symbol": symbol,
                    "fraction": widget["fraction"].get(),
                    "valence": valence,
                    "stoichiometry": float(stoichiometry),
                    "real_stoichiometry": float(stoichiometry)*fraction
                })

        num_anions = int(self.site_widgets["anion"]["combobox_num"].get())
        for i in range(num_anions):
            widget = self.site_widgets["anion"]["dynamic_widgets"][i]
            symbol = widget["symbol"].get()
            if symbol in used_symbols:
                self.show_error("Ошибка", f"Анион '{symbol}' повторяется")
                widget["symbol"].configure(background="#ffcccc")
                return None, None
            used_symbols.add(symbol)
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
            cb_symbol.grid(row=row_pos, column=2, sticky = 'ew', padx=5, pady=2)

            entry_fraction = tk.Entry(self.solvents_frame, width=10, **AppStyles.entry_style())
            entry_fraction.insert(0, "1")
            entry_fraction.grid(row=row_pos, column=3, sticky = 'ew', padx=5, pady=2)
            self.solvents_widgets[solvent_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.solvents_widgets)

    def create_solvent_properties(self):
        self.propereties_frame = tk.LabelFrame(self.first_column, text="свойства раствора",
                                               **AppStyles.labelframe_style())
        self.propereties_frame.pack(expand=True, fill = 'x', pady=5)
        self.propereties_frame.columnconfigure(0, weight=1)
        self.propereties_frame.columnconfigure(1, weight=1)
        self.propereties_frame.columnconfigure(2, weight=1)
        tk.Label(self.propereties_frame, text="Объем раствора",
                 **AppStyles.label_style()).grid(row=0, column=0, sticky = 'ew', padx=5, pady=2)
        tk.Label(self.propereties_frame, text="Концентрация раствора",
                 **AppStyles.label_style()).grid(row=0, column=1, sticky = 'ew', padx=5, pady=2)
        if self.antisolv_check.get() == 1:
            tk.Label(self.propereties_frame, text="Объем антирастворителя",
                 **AppStyles.label_style()).grid(row=0, column=2, sticky = 'ew', padx=5, pady=2)

        self.entry_v_solvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
        self.entry_v_solvent.grid(row=1, column=0, sticky = 'ew', padx=5, pady=2)
        self.entry_c_solvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
        self.entry_c_solvent.grid(row=1, column=1, sticky = 'ew', padx=5, pady=2)
        if self.antisolv_check.get() == 1:
            self.entry_v_antisolvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
            self.entry_v_antisolvent.grid(row=1, column=2, sticky = 'ew', padx=5, pady=2)

    def reset_form(self):

        for widget in self.first_column.winfo_children():
            widget.destroy()

        for widget in self.sec_column.winfo_children():
            widget.destroy()

        self.first_column.update()
        self.sec_column.update()

        for attr in ['sites_frame', 'solvents_frame', 'propereties_frame',
                     'k_factors_frame', 'data_apply_button_frame', 'results_frame',
                     'console_text', 'fav_button']:
            if hasattr(self, attr):
                delattr(self, attr)

        self.site_widgets = {}
        self.solvents_widgets = {}
        self.k_factors_widgets = {}
        self.dynamic_widgets = []
        self.create_template_frame()
        self.update()

    def show_error(self, title, message):
        tk.messagebox.showerror(title, message)
