import tkinter as tk
from tkinter import ttk, scrolledtext
from analysis.calculation_tests import show_error

from analysis.database_utils import (get_templates_list, get_template_id, get_template_sites,
                                     get_candidate_cations, get_solvents, get_anion_stoichiometry)
from gui.default_style import AppStyles
from gui.language.manager import localization_manager
from analysis.calculation_tests import float_test

class CompositionView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        localization_manager.register_observer(self)

        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.build_ui()
        self.create_template_frame()
        self.dynamic_widgets = []

    def build_ui(self):
        main_frame = tk.Frame(self, **AppStyles.frame_style())
        main_frame.pack(fill="both", expand=True)

        self.paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=5)

        first_column_container = tk.Frame(self.paned_window, **AppStyles.frame_style())
        self.paned_window.add(first_column_container, weight=1)

        canvas1 = tk.Canvas(first_column_container, borderwidth=0, highlightthickness=0)
        scrollbar1 = tk.Scrollbar(first_column_container, orient="vertical", command=canvas1.yview)

        scrollbar1.pack(side="right", fill="y")
        canvas1.pack(side="left", fill="both", expand=True)
        canvas1.configure(yscrollcommand=scrollbar1.set)

        self.first_column = tk.Frame(canvas1, **AppStyles.frame_style())
        canvas_window1 = canvas1.create_window((0, 0), window=self.first_column, anchor="nw")

        self.first_column.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
        canvas1.bind("<Configure>", lambda e: canvas1.itemconfig(canvas_window1, width=e.width))

        def bind_mousewheel1(event):
            canvas1.bind_all("<MouseWheel>", lambda e: canvas1.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def unbind_mousewheel1(event):
            canvas1.unbind_all("<MouseWheel>")

        self.first_column.bind("<Enter>", bind_mousewheel1)
        self.first_column.bind("<Leave>", unbind_mousewheel1)

        sec_column_container = tk.Frame(self.paned_window, **AppStyles.frame_style())
        self.paned_window.add(sec_column_container, weight=3)

        canvas2 = tk.Canvas(sec_column_container, borderwidth=0, highlightthickness=0)
        scrollbar2 = tk.Scrollbar(sec_column_container, orient="vertical", command=canvas2.yview)

        scrollbar2.pack(side="right", fill="y")
        canvas2.pack(side="left", fill="both", expand=True)
        canvas2.configure(yscrollcommand=scrollbar2.set)

        self.sec_column = tk.Frame(canvas2, **AppStyles.frame_style())
        canvas_window2 = canvas2.create_window((0, 0), window=self.sec_column, anchor="nw")

        self.sec_column.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))
        canvas2.bind("<Configure>", lambda e: canvas2.itemconfig(canvas_window2, width=e.width))

        def bind_mousewheel2(event):
            canvas2.bind_all("<MouseWheel>", lambda e: canvas2.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        def unbind_mousewheel2(event):
            canvas2.unbind_all("<MouseWheel>")

        self.sec_column.bind("<Enter>", bind_mousewheel2)
        self.sec_column.bind("<Leave>", unbind_mousewheel2)

    def create_template_frame(self):
        self.main_info_frame = tk.LabelFrame(self.first_column,
                                             text=localization_manager.tr("cfv_main_info_frame"),
                                             **AppStyles.labelframe_style())
        self.main_info_frame.pack(fill='x', pady=5)

        self.main_info_frame.columnconfigure(0, weight=1)
        self.main_info_frame.columnconfigure(1, weight=1)
        self.main_info_frame.columnconfigure(2, weight=1)

        phase_t = get_templates_list()
        data_type = ["",
                     localization_manager.tr("cfv_dt1"),
                     localization_manager.tr("cfv_dt2"),
                     localization_manager.tr("cfv_dt3")]
        device_type = [localization_manager.tr("ccv_device1"),
                       localization_manager.tr("ccv_device2"),
                        localization_manager.tr("ccv_device3"),
                        localization_manager.tr("ccv_device4"),
                        localization_manager.tr("ccv_device5"),
                        localization_manager.tr("ccv_device6"),
                        localization_manager.tr("ccv_device7"),
                        localization_manager.tr("ccv_device8"),
                        localization_manager.tr("ccv_device9")]

        self.mi_label1 = tk.Label(self.main_info_frame,
                                  text=localization_manager.tr("mi_label1"),
                                  **AppStyles.label_style())
        self.mi_label1.grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        self.entry_template = ttk.Combobox(self.main_info_frame,
                                           values=phase_t,
                                           **AppStyles.combobox_config())
        self.entry_template.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        self.mi_label2 = tk.Label(self.main_info_frame,
                                  text=localization_manager.tr("mi_label2"),
                                  **AppStyles.label_style())
        self.mi_label2.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.entry_data_type = ttk.Combobox(self.main_info_frame,
                                            values=data_type,
                                            **AppStyles.combobox_config())
        self.entry_data_type.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        self.mi_label3 = tk.Label(self.main_info_frame,
                                  text=localization_manager.tr("mi_label3"),
                                  **AppStyles.label_style())
        self.mi_label3.grid(row=0, column=2, sticky='ew', padx=5, pady=2)
        self.entry_device_type = ttk.Combobox(self.main_info_frame,
                                              values=device_type,
                                              **AppStyles.combobox_config())
        self.entry_device_type.grid(row=1, column=2, sticky='ew', padx=5, pady=2)

        self.mi_label4 = tk.Label(self.main_info_frame,
                                  text=localization_manager.tr("mi_label4"),
                                  **AppStyles.label_style())
        self.mi_label4.grid(row=2, column=0, sticky='ew', padx=5, pady=2)
        self.entry_doi = tk.Entry(self.main_info_frame,
                                  **AppStyles.entry_style())
        self.entry_doi.grid(row=3, column=0, sticky='ew', padx=5, pady=2)

        self.mi_label5 = tk.Label(self.main_info_frame,
                                  text=localization_manager.tr("mi_label5"),
                                  **AppStyles.label_style())
        self.mi_label5.grid(row=2, column=1, columnspan=2, sticky='ew', padx=5, pady=2)
        self.entry_name = tk.Entry(self.main_info_frame,
                                    **AppStyles.entry_style())
        self.entry_name.grid(row=3, column=1, columnspan=2, sticky='ew', padx=5, pady=2)

        self.mi_label6 = tk.Label(self.main_info_frame,
                                  text=localization_manager.tr("mi_label6"),
                                  **AppStyles.label_style())
        self.mi_label6.grid(row=4, column=0, columnspan=3, sticky='ew', padx=5, pady=2)
        self.entry_notes = tk.Entry(self.main_info_frame,
                                    **AppStyles.entry_style())
        self.entry_notes.grid(row=5, column=0, columnspan=3, sticky='ew', padx=5, pady=2)

        self.submit_button_frame = tk.Frame(self.first_column,
                                            **AppStyles.frame_style())
        self.submit_button_frame.pack(fill='x', pady=5)

        self.submit_button_frame.columnconfigure(0, weight=1)
        self.submit_button_frame.columnconfigure(1, weight=1)

        self.button_info_entry = tk.Button(self.submit_button_frame,
                                           text=localization_manager.tr("cfv_entry_but"),
                                           command=self.create_form,
                                           **AppStyles.button_style())
        self.button_info_entry.grid(row=0, column=0, sticky='ew', padx=5, pady=2)

        clear_btn = tk.Button(self.submit_button_frame,
                              text=localization_manager.tr("ucv_but6"),
                              **AppStyles.button_style(),
                              command=self.reset_form)
        clear_btn.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

    def create_form(self):
        device_type = self.entry_device_type.get()
        self.create_properties_frame(device_type)
        self.create_sites()
        self.create_solvents()
        self.create_k_factors_frame()
        self.create_solvent_properties()
        self.create_submit_button()

    def create_properties_frame(self, device_type):
        self.properties_frame = tk.LabelFrame(self.first_column,
                                              text=localization_manager.tr("cfv_prop"),
                                              **AppStyles.labelframe_style())
        self.properties_frame.pack(expand=True, fill='x', pady=5)
        self.property_labels = []
        self.property_entries = []
        self.properties_data = {}

        device_configs = {
            localization_manager.tr("ccv_device1"): (7, "dev1"),
            localization_manager.tr("ccv_device2"): (7, "dev2"),
            localization_manager.tr("ccv_device3"): (7, "dev3"),
            localization_manager.tr("ccv_device4"): (5, "dev4"),
            localization_manager.tr("ccv_device5"): (7, "dev5"),
            localization_manager.tr("ccv_device6"): (6, "dev6"),
            localization_manager.tr("ccv_device7"): (4, "dev7"),
            localization_manager.tr("ccv_device8"): (4, "dev8"),
            localization_manager.tr("ccv_device9"): (4, "dev9")
        }

        if device_type not in device_configs:
            return

        num_properties, dev_key = device_configs[device_type]

        for row in range(num_properties):
            label_text = localization_manager.tr(f"ccv_{dev_key}_prop{row + 1}")
            label = tk.Label(self.properties_frame, text=label_text, **AppStyles.label_style())
            label.grid(column=0, row=row)
            self.property_labels.append(label)

            entry = tk.Entry(self.properties_frame, **AppStyles.entry_style())
            entry.grid(column=1, row=row)
            self.property_entries.append(entry)

            setattr(self, f"ccv_{dev_key}_prop{row + 1}", entry)

    def clear_properties_frame(self):
        for widget in self.properties_frame.winfo_children():
            widget.destroy()

        self.property_labels.clear()
        self.property_entries.clear()
        self.properties_data.clear()


    def create_sites(self):
        self.button_info_entry["state"] = "disabled"
        self.structure_frame = tk.LabelFrame(self.sec_column,
                                             text=localization_manager.tr("ucv_lf4"),
                                             **AppStyles.labelframe_style())
        self.structure_frame.pack(expand=True, fill='x', pady=5)
        self.name = self.entry_template.get()
        self.template_id = get_template_id(self.name)
        sites_data = get_template_sites(self.template_id)
        self.anion_stoichiometry = get_anion_stoichiometry(self.template_id)
        values_sites = ["1", "2", "3", "4"]
        values_anions = ["1", "2", "3"]

        for field in self.structure_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        self.structure_frame.columnconfigure(0, weight=1)
        self.structure_frame.columnconfigure(1, weight=1)
        self.structure_frame.columnconfigure(2, weight=2)
        self.structure_frame.columnconfigure(3, weight=2)

        tk.Label(self.structure_frame,
                 text=localization_manager.tr("ucv_l5"),
                 **AppStyles.label_style()).grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        tk.Label(self.structure_frame,
                 text=localization_manager.tr("ucv_l6"),
                 **AppStyles.label_style()).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        tk.Label(self.structure_frame,
                 text=localization_manager.tr("ucv_l7"),
                 **AppStyles.label_style()).grid(row=0, column=2, sticky='ew', padx=5, pady=2)
        tk.Label(self.structure_frame,
                 text=localization_manager.tr("ucv_l8"),
                 **AppStyles.label_style()).grid(row=0, column=3, sticky='ew', padx=5, pady=2)

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

            label_site = tk.Label(self.structure_frame, text=site_type,
                                  **AppStyles.label_style())
            label_site.grid(row=current_row, column=0, padx=5, pady=2, sticky='ew')
            combobox_num = ttk.Combobox(
                self.structure_frame,
                values=values_sites,
                state="readonly",
                width=5,
                **AppStyles.combobox_config()
            )
            combobox_num.current(0)
            combobox_num.grid(row=current_row, column=1, padx=5, pady=2, sticky='ew')
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
        label_site = tk.Label(self.structure_frame, text=site_type,
                              **AppStyles.label_style())
        label_site.grid(row=current_row, column=0, padx=5, pady=2, sticky='ew')
        combobox_num = ttk.Combobox(
            self.structure_frame,
            values=values_anions,
            state="readonly",
            width=5,
            **AppStyles.combobox_config()
        )
        combobox_num.current(0)
        combobox_num.grid(row=current_row, column=1, padx=5, pady=2, sticky='ew')
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
                self.structure_frame,
                values=symbols,
                state="readonly"
                , **AppStyles.combobox_config()
            )
            if symbols:
                cb_symbol.current(0)
            cb_symbol.grid(row=row_pos, column=2, padx=5, pady=2, sticky='ew')

            entry_fraction = tk.Entry(self.structure_frame, width=10, **AppStyles.entry_style())
            entry_fraction.insert(0, "1")
            entry_fraction.grid(row=row_pos, column=3, padx=5, pady=2, sticky='ew')
            self.site_widgets[site_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.site_widgets)

    def recalculate_all_positions(self, widget):
        current_row = 1

        for site_type in widget:
            widget[site_type]["label"].grid(row=current_row, column=0, sticky='ew', padx=5, pady=2)
            widget[site_type]["combobox_num"].grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)

            for field in widget[site_type]["dynamic_widgets"]:
                field["symbol"].grid(row=current_row, column=2, sticky='ew', padx=5, pady=2)
                field["fraction"].grid(row=current_row, column=3, sticky='ew', padx=5, pady=2)
                current_row += 1

    def create_solvents(self):
        self.solvents_frame = tk.LabelFrame(self.sec_column,
                                            text=localization_manager.tr("ucv_lf5"),
                                            **AppStyles.labelframe_style())
        self.solvents_frame.pack(expand=True, fill='x', pady=5)
        self.solvents_frame.columnconfigure(0, weight=1)
        self.solvents_frame.columnconfigure(1, weight=1)
        self.solvent_types = ["solvent", "antisolvent"]

        values_solvents = ["1", "2"]

        for field in self.solvents_frame.winfo_children():
            field["symbol"].destroy()
            field["fraction"].destroy()

        tk.Label(self.solvents_frame,
                 text=localization_manager.tr("ucv_l9"),
                 **AppStyles.label_style()).grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        tk.Label(self.solvents_frame,
                 text=localization_manager.tr("ucv_l10"),
                 **AppStyles.label_style()).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        tk.Label(self.solvents_frame,
                 text=localization_manager.tr("ucv_l11"),
                 **AppStyles.label_style()).grid(row=0, column=2, sticky='ew', padx=5, pady=2)
        tk.Label(self.solvents_frame,
                 text=localization_manager.tr("ucv_l12"),
                 **AppStyles.label_style()).grid(row=0, column=3, sticky='ew', padx=5, pady=2)

        self.solvents_widgets = {}

        for type in self.solvent_types:
            if type == "solvent":
                text_type = localization_manager.tr("ucv_sol")
            else:
                text_type = localization_manager.tr("ucv_anti")
            current_row = self.get_next_row(self.solvents_widgets)
            label_solvent = tk.Label(self.solvents_frame, text=text_type,
                                     **AppStyles.label_style())
            label_solvent.grid(row=current_row, column=0, sticky='ew', padx=5, pady=2)
            combobox_num = ttk.Combobox(
                self.solvents_frame,
                values=values_solvents,
                state="readonly",
                width=5,
                **AppStyles.combobox_config()
            )
            combobox_num.current(0)
            combobox_num.grid(row=current_row, column=1, sticky='ew', padx=5, pady=2)
            combobox_num.bind(
                "<<ComboboxSelected>>",
                lambda e, t=type: self._update_solvent(t)
            )

            self.solvents_widgets[type] = {
                "label": label_solvent,
                "combobox_num": combobox_num,
                "dynamic_widgets": []
            }

            self._update_solvent(type)

    def create_k_factors_frame(self):
        self.current_row = 1
        self.k_factors_frame = tk.LabelFrame(self.sec_column,
                                             text=localization_manager.tr("ucv_lf6"),
                                             **AppStyles.labelframe_style())
        self.k_factors_frame.pack(expand=True, fill='x', pady=5)

        self.k_factors_frame.columnconfigure(0, weight=1)
        self.k_factors_frame.columnconfigure(1, weight=1)

        tk.Button(self.k_factors_frame,
                  text=localization_manager.tr("ucv_but9"),
                  command=self.create_k_factors_widgets,
                  **AppStyles.button_style()).grid(row=0, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(self.k_factors_frame,
                 text=localization_manager.tr("ucv_l13"),
                 **AppStyles.label_style()).grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(self.k_factors_frame,
                 text=localization_manager.tr("ucv_l14"),
                 **AppStyles.label_style()).grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        self.k_factors_widgets = {
            "dynamic_widgets": []
        }

    def create_k_factors_widgets(self):
        self.current_row += 1
        salt = tk.Entry(
            self.k_factors_frame,
            width=5,
            **AppStyles.entry_style()
        )
        salt.grid(row=self.current_row, column=0, sticky='ew', padx=5, pady=2)
        entry_k_factor = tk.Entry(self.k_factors_frame, width=10,
                                  **AppStyles.entry_style())
        entry_k_factor.grid(row=self.current_row, column=1, sticky='ew', padx=5, pady=2)
        self.k_factors_widgets["dynamic_widgets"].append({
            "salt": salt,
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
                    err = localization_manager.tr("ucv_error1")
                    show_error(f"{err} {symbol}")
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
            v_antisolvent = float(self.entry_v_antisolvent.get())
        except ValueError:
            show_error(message=localization_manager.tr("ucv_error2"))
            return
        stab_notes = self.entry_stab_notes.get()
        method_desc = self.entry_method_desc.get()
        solution_info = [stab_notes, v_antisolvent, v_solvent, c_solvent, method_desc]
        return solvents, solution_info

    def get_k_factors_data(self):
        used_salts = set()
        k_factors = []
        num_k_factors = len(self.k_factors_widgets["dynamic_widgets"])
        for i in range(num_k_factors):
            widget = self.k_factors_widgets["dynamic_widgets"][i]

            symbol = widget["salt"].get()

            if symbol in used_salts:
                err = localization_manager.tr("ucv_error3")
                show_error(f"{err} {symbol}")
                return None, None
            used_salts.add(symbol)
            k_factor = float_test(widget["k_factor"].get(),
                                  localization_manager.tr("ucv_lf6"))
            k_factors.append({
                "salt": widget["salt"].get(),
                "k_factor": k_factor,
            })
        return k_factors

    def get_structure_data(self):
        used_symbols = set()
        structure_data = []
        for idx, site_type in enumerate(self.structure_types):
            num_sites = int(self.site_widgets[site_type]["combobox_num"].get())
            valence = self.structure_valences[idx]
            stoichiometry = self.structure_stoichiometry[idx]
            for i in range(num_sites):
                widget = self.site_widgets[site_type]["dynamic_widgets"][i]
                fraction = float_test(widget["fraction"].get(),
                                      localization_manager.tr("ucv_l17"))
                if fraction is None:
                    return None, None
                symbol = widget["symbol"].get()
                if symbol in used_symbols:
                    err = localization_manager.tr("ucv_error4")
                    show_error(f"{err} {symbol}")
                    widget["symbol"].configure(background="#ffcccc")
                    return None, None
                used_symbols.add(symbol)
                structure_data.append({
                    "structure_type": site_type,
                    "symbol": symbol,
                    "fraction": widget["fraction"].get(),
                    "valence": valence
                })

        num_anions = int(self.site_widgets["anion"]["combobox_num"].get())
        for i in range(num_anions):
            widget = self.site_widgets["anion"]["dynamic_widgets"][i]
            symbol = widget["symbol"].get()
            if symbol in used_symbols:
                err = localization_manager.tr("ucv_error5")
                show_error(f"{err} {symbol}")
                widget["symbol"].configure(background="#ffcccc")
                return None, None
            used_symbols.add(symbol)
            structure_data.append({
                "structure_type": "anion",
                "valence": 1,
                "symbol": widget["symbol"].get(),
                "fraction": widget["fraction"].get(),
            })
        return structure_data

    def collect_properties_data(self):
        data = []
        for entry in self.property_entries:
            data.append(entry.get())
        return data

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
                **AppStyles.combobox_config()
            )
            if symbols:
                cb_symbol.current(0)
            cb_symbol.grid(row=row_pos, column=2, sticky='ew', padx=5, pady=2)

            entry_fraction = tk.Entry(self.solvents_frame, width=10, **AppStyles.entry_style())
            entry_fraction.insert(0, "1")
            entry_fraction.grid(row=row_pos, column=3, sticky='ew', padx=5, pady=2)
            self.solvents_widgets[solvent_type]["dynamic_widgets"].append({
                "symbol": cb_symbol,
                "fraction": entry_fraction
            })

        self.recalculate_all_positions(self.solvents_widgets)

    def create_solvent_properties(self):
        self.propereties_frame = tk.LabelFrame(self.sec_column,
                                               text=localization_manager.tr("ucv_l18"),
                                               **AppStyles.labelframe_style())
        self.propereties_frame.pack(expand=True, fill='x', pady=5)

        tk.Label(self.propereties_frame,
                 text=localization_manager.tr("ucv_l19"),
                 **AppStyles.label_style()).grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        tk.Label(self.propereties_frame,
                 text=localization_manager.tr("ucv_l20"),
                 **AppStyles.label_style()).grid(row=1, column=0, sticky='ew', padx=5, pady=2)
        tk.Label(self.propereties_frame,
                 text=localization_manager.tr("ucv_l21"),
                 **AppStyles.label_style()).grid(row=2, column=0, sticky='ew', padx=5, pady=2)
        tk.Label(self.propereties_frame,
                 text="Stability notes",
                 **AppStyles.label_style()).grid(row=3, column=0, sticky='ew', padx=5, pady=2)
        tk.Label(self.propereties_frame,
                 text="Method description",
                 **AppStyles.label_style()).grid(row=4, column=0, sticky='ew', padx=5, pady=2)

        self.entry_v_solvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
        self.entry_v_solvent.grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        self.entry_c_solvent = tk.Entry(self.propereties_frame, width=10,
                                        **AppStyles.entry_style())
        self.entry_c_solvent.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        self.entry_v_antisolvent = tk.Entry(self.propereties_frame, width=10,
                                            **AppStyles.entry_style())
        self.entry_v_antisolvent.grid(row=2, column=1, sticky='ew', padx=5, pady=2)

        self.entry_stab_notes = tk.Entry(self.propereties_frame, width=10,
                                         **AppStyles.entry_style())
        self.entry_stab_notes.grid(row=3, column=1, sticky='ew', padx=5, pady=2)

        self.entry_method_desc = tk.Entry(self.propereties_frame, width=10,
                                         **AppStyles.entry_style())
        self.entry_method_desc.grid(row=4, column=1, sticky='ew', padx=5, pady=2)

    def create_submit_button(self):
        self.subm_button = tk.Button(self.sec_column,
                                    text=localization_manager.tr("cfv_upl_but"),
                                    command = self.upload_data,
                                    **AppStyles.button_style())
        self.subm_button.pack(expand=True, fill='x', pady=5)

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

    def upload_data(self):
        solvents, solution_info = self.get_solution_data()
        k_factors = self.get_k_factors_data()
        structure_data = self.get_structure_data()
        properties = self.collect_properties_data()
        main_info = [self.entry_device_type.get(),
                     self.entry_doi.get(),
                     self.entry_data_type.get(),
                     self.entry_notes.get(),
                     self.entry_name.get()]
        self.controller.handle_main_submit(main_info,  solution_info, structure_data,
                           solvents, properties, k_factors)
