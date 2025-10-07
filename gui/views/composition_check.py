import tkinter as tk
from tkinter import ttk
from gui.default_style import AppStyles
from gui.language.manager import localization_manager


class CompositionCheckView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        localization_manager.register_observer(self)
        self.title(localization_manager.tr("ccv_window_title"))
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.geometry("1200x700")
        self.build_ui()

    def build_ui(self):
        main_container = tk.Frame(self, **AppStyles.frame_style())
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Настраиваем колонки: первая в 2 раза больше правой
        main_container.columnconfigure(0, weight=2)  # Левая колонка - 2/3
        main_container.columnconfigure(1, weight=1)  # Правая колонка - 1/3
        main_container.rowconfigure(0, weight=1)

        # ЛЕВАЯ КОЛОНКА - композиции и избранное
        left_column = tk.Frame(main_container, **AppStyles.frame_style())
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_column.columnconfigure(0, weight=1)
        left_column.rowconfigure(0, weight=1)  # Первое дерево
        left_column.rowconfigure(1, weight=1)  # Второе дерево

        # Первое дерево - композиции
        compositions_frame = tk.LabelFrame(left_column,
                                           text=localization_manager.tr("ccv_comp_frame"),
                                           **AppStyles.labelframe_style())
        compositions_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        compositions_frame.columnconfigure(0, weight=1)
        compositions_frame.rowconfigure(0, weight=1)

        # Второе дерево - избранное
        favorites_frame = tk.LabelFrame(left_column,
                                        text=localization_manager.tr("ccv_fav_frame"),
                                        **AppStyles.labelframe_style())
        favorites_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        favorites_frame.columnconfigure(0, weight=1)
        favorites_frame.rowconfigure(0, weight=1)

        # ПРАВАЯ КОЛОНКА - детали
        right_column = tk.Frame(main_container, **AppStyles.frame_style())
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_column.columnconfigure(0, weight=1)
        right_column.rowconfigure(0, weight=1)

        details_frame = tk.LabelFrame(right_column,
                                      text=localization_manager.tr("ccv_det_frame"),
                                      **AppStyles.labelframe_style())
        details_frame.grid(row=0, column=0, sticky="nsew")
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)

        # НАСТРОЙКА ДЕРЕВЬЕВ В ЛЕВОЙ КОЛОНКЕ

        # Дерево композиций
        self.comp_columns = (localization_manager.tr("ccv_comp_col_id"),
                             localization_manager.tr("ccv_comp_col_name"),
                             localization_manager.tr("ccv_comp_col_device_type"),
                             localization_manager.tr("ccv_comp_col_doi"),
                             localization_manager.tr("ccv_comp_col_data"),
                             localization_manager.tr("ccv_comp_col_notes"),
                             localization_manager.tr("ccv_comp_col_template"))

        comp_container = tk.Frame(compositions_frame, **AppStyles.frame_style())
        comp_container.grid(row=0, column=0, sticky="nsew")
        comp_container.columnconfigure(0, weight=1)
        comp_container.rowconfigure(0, weight=1)
        comp_container.rowconfigure(1, weight=0)

        self.comp_tree = ttk.Treeview(comp_container, columns=self.comp_columns,
                                      show='headings', height=8,
                                      **AppStyles.treeview_config())

        for col in self.comp_columns:
            self.comp_tree.heading(col, text=col)
            self.comp_tree.column(col, width=80, stretch=True)

        comp_v_scrollbar = ttk.Scrollbar(comp_container, orient=tk.VERTICAL,
                                         command=self.comp_tree.yview)
        comp_h_scrollbar = ttk.Scrollbar(comp_container, orient=tk.HORIZONTAL,
                                         command=self.comp_tree.xview)

        self.comp_tree.configure(yscrollcommand=comp_v_scrollbar.set,
                                 xscrollcommand=comp_h_scrollbar.set)

        self.comp_tree.grid(row=0, column=0, sticky="nsew")
        comp_v_scrollbar.grid(row=0, column=1, sticky="ns")
        comp_h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Дерево избранного
        fav_container = tk.Frame(favorites_frame, **AppStyles.frame_style())
        fav_container.grid(row=0, column=0, sticky="nsew")
        fav_container.columnconfigure(0, weight=1)
        fav_container.rowconfigure(0, weight=1)
        fav_container.rowconfigure(1, weight=0)

        self.fav_columns = (localization_manager.tr("ccv_fav_col_id"),
                            localization_manager.tr("ccv_fav_col_name"),
                            localization_manager.tr("ccv_fav_col_phase_id"),
                            localization_manager.tr("ccv_fav_col_data"),
                            localization_manager.tr("ccv_fav_col_v_sol"),
                            localization_manager.tr("ccv_fav_col_v_antisol"),
                            localization_manager.tr("ccv_fav_col_conc"),
                            localization_manager.tr("ccv_fav_col_notes"),
                            )
        self.fav_tree = ttk.Treeview(fav_container, columns=self.fav_columns,
                                     show='headings', height=8,
                                     **AppStyles.treeview_config())

        for col in self.fav_columns:
            self.fav_tree.heading(col, text=col)
            self.fav_tree.column(col, width=80, stretch=True)

        fav_v_scrollbar = ttk.Scrollbar(fav_container, orient=tk.VERTICAL,
                                        command=self.fav_tree.yview)
        fav_h_scrollbar = ttk.Scrollbar(fav_container, orient=tk.HORIZONTAL,
                                        command=self.fav_tree.xview)

        self.fav_tree.configure(yscrollcommand=fav_v_scrollbar.set,
                                xscrollcommand=fav_h_scrollbar.set)

        self.fav_tree.grid(row=0, column=0, sticky="nsew")
        fav_v_scrollbar.grid(row=0, column=1, sticky="ns")
        fav_h_scrollbar.grid(row=1, column=0, sticky="ew")

        # НАСТРОЙКА ДЕТАЛЕЙ В ПРАВОЙ КОЛОНКЕ

        details_container = tk.Frame(details_frame, **AppStyles.frame_style())
        details_container.grid(row=0, column=0, sticky="nsew")
        details_container.columnconfigure(0, weight=1)
        details_container.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(details_container)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.main_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.solvents_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.structure_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.synthesis_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.properties_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.kfactors_tab = tk.Frame(self.notebook, **AppStyles.frame_style())

        self.notebook.add(self.main_tab, text=localization_manager.tr("ccv_main_tab"))
        self.notebook.add(self.solvents_tab, text=localization_manager.tr("ccv_solvents_tab"))
        self.notebook.add(self.structure_tab, text=localization_manager.tr("ccv_structure_tab"))
        self.notebook.add(self.synthesis_tab, text=localization_manager.tr("ccv_synthesis_tab"))
        self.notebook.add(self.properties_tab, text=localization_manager.tr("ccv_properties_tab"))
        self.notebook.add(self.kfactors_tab, text=localization_manager.tr("ccv_kfactors_tab"))

        # ПАНЕЛЬ УПРАВЛЕНИЯ
        control_frame = tk.Frame(main_container, **AppStyles.frame_style())
        control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=0)
        control_frame.columnconfigure(2, weight=1)

        tk.Button(control_frame,
                  text=localization_manager.tr("ccv_refresh_button"),
                  command=self.controller.refresh_all,
                  **AppStyles.button_style()).grid(row=0, column=1, padx=5, pady=5)

        # ПРИВЯЗКА СОБЫТИЙ
        self.comp_tree.bind('<<TreeviewSelect>>', self.on_composition_select)
        self.fav_tree.bind('<<TreeviewSelect>>', self.on_favorite_select)

    def on_composition_select(self, event):
        selection = self.comp_tree.selection()
        if selection:
            item = self.comp_tree.item(selection[0])
            composition_id = item['values'][0]
            self.controller.load_composition_details(composition_id)

    def on_favorite_select(self, event):
        selection = self.fav_tree.selection()
        if selection:
            item = self.fav_tree.item(selection[0])
            favorite_id = item['values'][0]
            self.controller.load_favorite_details(favorite_id)

    def display_compositions(self, data):
        self.comp_tree.delete(*self.comp_tree.get_children())
        for row in data:
            self.comp_tree.insert('', 'end', values=row)

    def display_favorites(self, data):
        self.fav_tree.delete(*self.fav_tree.get_children())
        for row in data:
            self.fav_tree.insert('', 'end', values=row)

    def display_details(self, details, is_favorite=False):
        self.clear_tabs()

        if details:
            self.display_main_info(details['main_info'], is_favorite)
            self.display_solvents(details['solvents'])
            self.display_structure(details['structure'])
            self.display_synthesis(details.get('synthesis'))

            if not is_favorite and details.get('properties'):
                self.display_properties(details['properties'])

            self.display_k_factors(details['k_factors'])

    def display_main_info(self, main_info, is_favorite):
        if main_info:
            for widget in self.main_tab.winfo_children():
                widget.destroy()

            # Создаем фрейм для основной информации с прокруткой
            main_frame = tk.Frame(self.main_tab, **AppStyles.frame_style())
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Создаем Canvas и Scrollbar для прокрутки
            canvas = tk.Canvas(main_frame, bg=AppStyles.BACKGROUND_COLOR, highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, **AppStyles.frame_style())

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y")

            # Определяем метки в зависимости от типа записи
            if is_favorite:
                labels = self.fav_columns
            else:
                labels = [
                    localization_manager.tr("ccv_comp_col_id"),
                    localization_manager.tr("ccv_comp_col_name"),
                    localization_manager.tr("ccv_comp_col_device_type"),
                    localization_manager.tr("ccv_comp_col_doi"),
                    localization_manager.tr("ccv_comp_col_data"),
                    localization_manager.tr("ccv_comp_col_notes"),
                    localization_manager.tr("ccv_comp_col_template")
                ]

            for i, (label, value) in enumerate(zip(labels, main_info)):
                label_widget = tk.Label(scrollable_frame, text=f"{label}:",
                                        anchor=tk.W, **AppStyles.label_style())
                label_widget.grid(row=i, column=0, sticky="w", padx=2, pady=1)

                value_widget = tk.Label(scrollable_frame, text=str(value) if value else '',
                                        anchor=tk.W, **AppStyles.label_style())
                value_widget.grid(row=i, column=1, sticky="w", padx=2, pady=1)

    def display_solvents(self, solvents):
        for widget in self.solvents_tab.winfo_children():
            widget.destroy()

        if solvents:
            columns = (localization_manager.tr("ccv_solv_col_type"),
                       localization_manager.tr("ccv_solv_col_symbol"),
                       localization_manager.tr("ccv_solv_col_fraction"))
            tree = self.create_treeview(self.solvents_tab, columns)
            for solvent in solvents:
                tree.insert('', 'end', values=solvent)
        else:
            tk.Label(self.solvents_tab, text="No solvents data",
                     **AppStyles.label_style()).pack(expand=True)

    def display_structure(self, structure):
        for widget in self.structure_tab.winfo_children():
            widget.destroy()

        if structure:
            columns = (localization_manager.tr("ccv_struct_col_type"),
                       localization_manager.tr("ccv_struct_col_symbol"),
                       localization_manager.tr("ccv_struct_col_fraction"),
                       localization_manager.tr("ccv_struct_col_val"))
            tree = self.create_treeview(self.structure_tab, columns)
            for element in structure:
                tree.insert('', 'end', values=element)
        else:
            tk.Label(self.structure_tab, text="No structure data",
                     **AppStyles.label_style()).pack(expand=True)

    def display_synthesis(self, synthesis):
        for widget in self.synthesis_tab.winfo_children():
            widget.destroy()

        if synthesis:
            # Создаем фрейм с прокруткой для синтеза
            main_frame = tk.Frame(self.synthesis_tab, **AppStyles.frame_style())
            main_frame.pack(fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(main_frame, bg=AppStyles.BACKGROUND_COLOR, highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, **AppStyles.frame_style())

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y")

            labels = [
                localization_manager.tr("ccv_synth_col_stab_notes"),
                localization_manager.tr("ccv_synth_col_v_antisol"),
                localization_manager.tr("ccv_synth_col_v_sol"),
                localization_manager.tr("ccv_synth_col_conc"),
                localization_manager.tr("ccv_synth_col_method")
            ]

            for i, (label, value) in enumerate(zip(labels, synthesis[1:])):  # Пропускаем id_info
                label_widget = tk.Label(scrollable_frame, text=f"{label}:",
                                        anchor=tk.W, **AppStyles.label_style())
                label_widget.grid(row=i, column=0, sticky="w", padx=2, pady=1)

                value_widget = tk.Label(scrollable_frame, text=str(value) if value else '',
                                        anchor=tk.W, **AppStyles.label_style())
                value_widget.grid(row=i, column=1, sticky="w", padx=2, pady=1)
        else:
            tk.Label(self.synthesis_tab, text="No synthesis data",
                     **AppStyles.label_style()).pack(expand=True)

    def display_properties(self, properties):
        for widget in self.properties_tab.winfo_children():
            widget.destroy()

        if properties:
            # Создаем фрейм с прокруткой для свойств
            main_frame = tk.Frame(self.properties_tab, **AppStyles.frame_style())
            main_frame.pack(fill=tk.BOTH, expand=True)

            canvas = tk.Canvas(main_frame, bg=AppStyles.BACKGROUND_COLOR, highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, **AppStyles.frame_style())

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y")

            # Здесь можно добавить специфичные метки для разных типов устройств
            labels = [f"Property {i + 1}" for i in range(len(properties))]

            row = 0
            for i, value in enumerate(properties):
                if value is not None:
                    label_widget = tk.Label(scrollable_frame, text=f"{labels[i]}:",
                                            anchor=tk.W, **AppStyles.label_style())
                    label_widget.grid(row=row, column=0, sticky="w", padx=2, pady=1)

                    value_widget = tk.Label(scrollable_frame, text=str(value),
                                            anchor=tk.W, **AppStyles.label_style())
                    value_widget.grid(row=row, column=1, sticky="w", padx=2, pady=1)
                    row += 1
        else:
            tk.Label(self.properties_tab, text="No properties data",
                     **AppStyles.label_style()).pack(expand=True)

    def display_k_factors(self, k_factors):
        for widget in self.kfactors_tab.winfo_children():
            widget.destroy()

        if k_factors:
            columns = (localization_manager.tr("ccv_k_col_salt"),
                       localization_manager.tr("ccv_k_col_k_fact"))
            tree = self.create_treeview(self.kfactors_tab, columns)
            for factor in k_factors:
                tree.insert('', 'end', values=factor)
        else:
            tk.Label(self.kfactors_tab, text="No K-factors data",
                     **AppStyles.label_style()).pack(expand=True)

    def create_treeview(self, parent, columns):
        container = tk.Frame(parent, **AppStyles.frame_style())
        container.pack(fill=tk.BOTH, expand=True)

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=0)

        tree = ttk.Treeview(container, columns=columns, show='headings',
                            **AppStyles.treeview_config())

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, stretch=True)

        v_scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=tree.xview)

        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        return tree

    def clear_tabs(self):
        for tab in [self.main_tab, self.solvents_tab, self.structure_tab,
                    self.synthesis_tab, self.properties_tab, self.kfactors_tab]:
            for widget in tab.winfo_children():
                widget.destroy()