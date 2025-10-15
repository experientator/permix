import tkinter as tk
from tkinter import ttk
from gui.default_style import AppStyles
import tkinter.messagebox as mb
from gui.language.manager import localization_manager

class SolventsCheckView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        localization_manager.register_observer(self)

        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()

        self.title(localization_manager.tr("scv_window_title"))

        self.build_ui()

    def build_ui(self):
        self.main_frame = tk.Frame(self, **AppStyles.frame_style())
        self.main_frame.pack(fill="both", expand=True)

        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=5)

        first_col_frame = tk.Frame(self.paned_window)
        self.paned_window.add(first_col_frame, weight=2)

        tree_container = tk.Frame(first_col_frame)
        tree_container.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_container)
        scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_container,
                                 columns=('name', 'type', 'formula', 'density', 'boiling_point', 'notes'),
                                 show='headings',
                                 yscrollcommand=scrollbar.set,
                                 **AppStyles.treeview_config())
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading('name', text=localization_manager.tr("scv_sol_col_name"))
        self.tree.heading('type', text=localization_manager.tr("scv_sol_col_type"))
        self.tree.heading('formula', text=localization_manager.tr("scv_sol_col_formula"))
        self.tree.heading('density', text=localization_manager.tr("scv_sol_col_density"))
        self.tree.heading('boiling_point', text=localization_manager.tr("scv_sol_col_temp"))
        self.tree.heading('notes', text=localization_manager.tr("scv_sol_col_notes"))

        self.tree.column('name', width=150, anchor='center')
        self.tree.column('type', width=100, anchor='center')
        self.tree.column('formula', width=100, anchor='center')
        self.tree.column('density', width=100, anchor='center')
        self.tree.column('boiling_point', width=150, anchor='center')
        self.tree.column('notes', width=200, anchor='center')

        delete_frame = tk.Frame(first_col_frame)
        delete_frame.pack(fill="x", pady=5)

        delete_btn = tk.Button(delete_frame,
                               text=localization_manager.tr("icv_delete_button"),
                               command=self.controller.delete_selected,
                               **AppStyles.button_style())
        delete_btn.pack(fill="x", padx=10)

        second_col_frame = tk.Frame(self.paned_window)
        self.paned_window.add(second_col_frame, weight=1)

        form_frame = tk.LabelFrame(second_col_frame,
                                   text=localization_manager.tr("scv_add_sol_frame"),
                                   **AppStyles.labelframe_style())
        form_frame.pack(fill="both", expand=True)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=1)

        tk.Label(form_frame,
                 text=localization_manager.tr("scv_sol_col_name"),
                 **AppStyles.label_style()).grid(row=0, column=0, sticky='ew', padx=5,
                                                                              pady=2)
        self.entry_name = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("scv_sol_col_type"),
                 **AppStyles.label_style()).grid(row=0, column=1, sticky='ew', padx=5, pady=2)

        self.box_solvent_type = ttk.Combobox(form_frame,
                                             values=[localization_manager.tr("scv_sol_form_cb_solv"),
                                                     localization_manager.tr("scv_sol_form_cb_anti")],
                                             **AppStyles.combobox_config())
        self.box_solvent_type.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        self.box_solvent_type.current(0)

        tk.Label(form_frame,
                 text=localization_manager.tr("scv_sol_col_formula"),
                 **AppStyles.label_style()).grid(row=2, column=0, sticky='ew', padx=5,
                                                                             pady=2)
        self.entry_formula = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_formula.grid(row=3, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("scv_sol_col_density"),
                 **AppStyles.label_style()).grid(row=2, column=1, sticky='ew',padx=5, pady=2)
        self.entry_density = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_density.grid(row=3, column=1, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("scv_sol_col_temp"),
                 **AppStyles.label_style()).grid(row=4, column=0, sticky='ew', padx=5, pady=2)
        self.entry_bp = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_bp.grid(row=5, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("scv_sol_col_notes"),
                 **AppStyles.label_style()).grid(row=4, column=1, sticky='ew', padx=5,
                                                                             pady=2)
        self.entry_notes = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_notes.grid(row=5, column=1, sticky='ew', padx=5, pady=2)

        button_frame = tk.Frame(second_col_frame)
        button_frame.pack(fill="x", pady=5)

        upload_btn = tk.Button(button_frame,
                               text=localization_manager.tr("scv_upload_button"),
                               command=self.on_submit,
                               **AppStyles.button_style())
        upload_btn.pack(fill="x", padx=5)

    def on_submit(self):
        type = ""
        if self.box_solvent_type.get() == localization_manager.tr("scv_sol_form_cb_solv"):
            type = "solvent"
        elif self.box_solvent_type.get() == localization_manager.tr("scv_sol_form_cb_anti"):
            type = "antisolvent"

        data = {
            'name': self.entry_name.get(),
            'type': type,
            'formula': self.entry_formula.get(),
            'density': self.entry_density.get(),
            'boiling_point': self.entry_bp.get(),
            'notes': self.entry_notes.get()
        }
        self.controller.handle_submit(data)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.box_solvent_type.set(localization_manager.tr("scv_sol_form_cb_solv"))
        self.entry_formula.delete(0, tk.END)
        self.entry_density.delete(0, tk.END)
        self.entry_bp.delete(0, tk.END)
        self.entry_notes.delete(0, tk.END)

    def show_data(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in data:
            self.tree.insert('', 'end', values=row)

    def get_selected_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        return self.tree.item(selected_item)
