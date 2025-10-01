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
        self.attributes('-fullscreen', True)
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.build_ui()
        menu = tk.Menu(self)
        menu.add_command(label=localization_manager.tr("menu_exit"),
                         command=self.destroy)
        self.config(menu=menu)

    def build_ui(self):

        main_container = tk.Frame(self, **AppStyles.frame_style())
        main_container.pack(fill=tk.BOTH, expand=True)

        main_container.columnconfigure(0, weight=1, minsize=350)
        main_container.columnconfigure(1, weight=1, minsize=350)
        main_container.columnconfigure(2, weight=2, minsize=500)
        main_container.rowconfigure(0, weight=1)

        compositions_frame = tk.LabelFrame(main_container,
                                           text=localization_manager.tr("ccv_comp_frame"),
                                           **AppStyles.labelframe_style())
        compositions_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        compositions_frame.columnconfigure(0, weight=1)
        compositions_frame.rowconfigure(0, weight=1)

        favorites_frame = tk.LabelFrame(main_container,
                                        text=localization_manager.tr("ccv_fav_frame"),
                                        **AppStyles.labelframe_style())
        favorites_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        favorites_frame.columnconfigure(0, weight=1)
        favorites_frame.rowconfigure(0, weight=1)

        details_frame = tk.LabelFrame(main_container,
                                      text=localization_manager.tr("ccv_det_frame"),
                                      **AppStyles.labelframe_style())
        details_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)

        self.comp_columns = (localization_manager.tr("ccv_comp_col_id"),
                        localization_manager.tr("ccv_comp_col_name"),
                        localization_manager.tr("ccv_comp_col_doi"),
                        localization_manager.tr("ccv_comp_col_data"),
                        localization_manager.tr("ccv_comp_col_notes"),
                        localization_manager.tr("ccv_comp_col_template"))

        self.comp_tree = ttk.Treeview(compositions_frame, columns=self.comp_columns,
                                      show='headings', height=15, **AppStyles.treeview_config())

        for col in self.comp_columns:
            self.comp_tree.heading(col, text=col)
            self.comp_tree.column(col, width=80, stretch=False)

        comp_container = tk.Frame(compositions_frame,
                                  **AppStyles.frame_style())
        comp_container.grid(row=0, column=0, sticky="nsew")
        comp_container.columnconfigure(0, weight=1)
        comp_container.rowconfigure(0, weight=1)
        comp_container.rowconfigure(1, weight=0)

        self.comp_tree = ttk.Treeview(comp_container, columns=self.comp_columns,
                                      show='headings', height=15,
                                      **AppStyles.treeview_config())

        for col in self.comp_columns:
            self.comp_tree.heading(col, text=col)
            self.comp_tree.column(col, width=100, stretch=False)

        comp_v_scrollbar = ttk.Scrollbar(comp_container, orient=tk.VERTICAL,
                                         command=self.comp_tree.yview)
        comp_h_scrollbar = ttk.Scrollbar(comp_container, orient=tk.HORIZONTAL,
                                         command=self.comp_tree.xview)

        self.comp_tree.configure(yscrollcommand=comp_v_scrollbar.set,
                                 xscrollcommand=comp_h_scrollbar.set)

        self.comp_tree.grid(row=0, column=0, sticky="nsew")
        comp_v_scrollbar.grid(row=0, column=1, sticky="ns")
        comp_h_scrollbar.grid(row=1, column=0, sticky="ew")

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
                                     show='headings', height=15)

        for col in self.fav_columns:
            self.fav_tree.heading(col, text=col)
            self.fav_tree.column(col, width=100, stretch=False)

        fav_v_scrollbar = ttk.Scrollbar(fav_container, orient=tk.VERTICAL,
                                        command=self.fav_tree.yview)
        fav_h_scrollbar = ttk.Scrollbar(fav_container, orient=tk.HORIZONTAL,
                                        command=self.fav_tree.xview)

        self.fav_tree.configure(yscrollcommand=fav_v_scrollbar.set,
                                xscrollcommand=fav_h_scrollbar.set)

        self.fav_tree.grid(row=0, column=0, sticky="nsew")
        fav_v_scrollbar.grid(row=0, column=1, sticky="ns")
        fav_h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.notebook = ttk.Notebook(details_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.main_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.solvents_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.structure_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.properties_tab = tk.Frame(self.notebook, **AppStyles.frame_style())
        self.kfactors_tab = tk.Frame(self.notebook, **AppStyles.frame_style())

        self.notebook.add(self.main_tab,
                          text=localization_manager.tr("ccv_main_tab"))
        self.notebook.add(self.solvents_tab,
                          text=localization_manager.tr("ccv_solvents_tab"))
        self.notebook.add(self.structure_tab,
                          text=localization_manager.tr("ccv_structure_tab"))
        self.notebook.add(self.properties_tab,
                          text=localization_manager.tr("ccv_properties_tab"))
        self.notebook.add(self.kfactors_tab,
                          text=localization_manager.tr("ccv_kfactors_tab"))

        control_frame = tk.Frame(main_container, **AppStyles.frame_style())
        control_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)

        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=0)
        control_frame.columnconfigure(2, weight=1)

        tk.Button(control_frame,
                  text=localization_manager.tr("ccv_refresh_button"),
                  command=self.controller.refresh_all,
                  **AppStyles.button_style()).grid(row=0, column=1, padx=5)

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

            if not is_favorite and 'properties' in details:
                self.display_properties(details['properties'])

            self.display_k_factors(details['k_factors'])

    def display_main_info(self, main_info, is_favorite):
        if main_info:
            for widget in self.main_tab.winfo_children():
                widget.destroy()

            grid_frame = tk.Frame(self.main_tab, **AppStyles.frame_style())
            grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            grid_frame.columnconfigure(0, weight=0, minsize=120)
            grid_frame.columnconfigure(1, weight=1, minsize=200)

            if is_favorite:
                labels = self.fav_columns
            else:
                labels = self.comp_columns

            for i, (label, value) in enumerate(zip(labels, main_info)):
                label_widget = tk.Label(grid_frame, text=f"{label}:",
                                         anchor=tk.W, **AppStyles.label_style())
                label_widget.grid(row=i, column=0, sticky="w", padx=2, pady=1)

                value_widget = tk.Label(grid_frame, text=str(value) if value else '',
                                         anchor=tk.W, **AppStyles.label_style())
                value_widget.grid(row=i, column=1, sticky="w", padx=2, pady=1)

    def display_solvents(self, solvents):
        if solvents:
            columns = (localization_manager.tr("ccv_solv_col_type"),
                       localization_manager.tr("ccv_solv_col_symbol"),
                       localization_manager.tr("ccv_solv_col_fraction"))
            tree = self.create_treeview(self.solvents_tab, columns)
            for solvent in solvents:
                tree.insert('', 'end', values=solvent)

    def display_structure(self, structure):
        if structure:
            columns = (localization_manager.tr("ccv_struct_col_type"),
                       localization_manager.tr("ccv_struct_col_symbol"),
                       localization_manager.tr("ccv_struct_col_fraction"),
                       localization_manager.tr("ccv_struct_col_val"))
            tree = self.create_treeview(self.structure_tab, columns)

            for element in structure:
                tree.insert('', 'end', values=element)

    def display_properties(self, properties):
        if properties:
            labels = [localization_manager.tr("ccv_prop_col_id"),
                      localization_manager.tr("ccv_prop_col_an_stoich"),
                      localization_manager.tr("ccv_prop_col_bg"),
                      localization_manager.tr("ccv_prop_col_ff"),
                      localization_manager.tr("ccv_prop_col_pse"),
                      localization_manager.tr("ccv_prop_col_voc"),
                      localization_manager.tr("ccv_prop_col_jsc"),
                      localization_manager.tr("ccv_prop_col_stab_notes"),
                      localization_manager.tr("ccv_prop_col_v_antisol"),
                      localization_manager.tr("ccv_prop_col_v_sol"),
                      localization_manager.tr("ccv_prop_col_conc"),
                      localization_manager.tr("ccv_prop_col_method")]

            for i, (label, value) in enumerate(zip(labels, properties)):
                tk.Label(self.properties_tab, text=f"{label}:"
                         , **AppStyles.label_style()).grid(row=i, column=0)
                tk.Label(self.properties_tab, text=str(value) if value else '',
                         **AppStyles.label_style()).grid(row=i, column=1)

    def display_k_factors(self, k_factors):
        if k_factors:
            columns = (localization_manager.tr("ccv_k_col_salt"),
                       localization_manager.tr("ccv_k_col_k_fact"))
            tree = self.create_treeview(self.kfactors_tab, columns)

            for factor in k_factors:
                tree.insert('', 'end', values=factor)

    def create_treeview(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show='headings',
                            **AppStyles.treeview_config())

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        return tree

    def clear_tabs(self):
        for tab in [self.main_tab, self.solvents_tab, self.structure_tab,
                    self.properties_tab, self.kfactors_tab]:
            for widget in tab.winfo_children():
                widget.destroy()

