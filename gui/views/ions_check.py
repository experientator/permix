import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from gui.default_style import AppStyles
from gui.language.manager import localization_manager

class IonsCheckView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        localization_manager.register_observer(self)
        self.title(localization_manager.tr("ccv_window_title"))
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label=localization_manager.tr("menu_exit"),
                         command=self.destroy)
        self.config(menu=menu)
        self.styles = AppStyles()
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, **AppStyles.frame_style())
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        left_frame = tk.Frame(main_frame, **AppStyles.frame_style())
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)

        ions_frame = tk.LabelFrame(left_frame,
                                   text=localization_manager.tr("icv_ions_frame"),
                                   **AppStyles.labelframe_style())
        ions_frame.grid(row=0, column=0, sticky="nsew")
        ions_frame.grid_columnconfigure(0, weight=1)
        ions_frame.grid_rowconfigure(0, weight=1)

        self.ions_tree = ttk.Treeview(
            ions_frame,
            columns=('name', 'type'),
            show='headings',
            **AppStyles.treeview_config()
        )
        self.ions_tree.heading('name',
                               text=localization_manager.tr("icv_solv_col_name"),
                               **AppStyles.treeview_headings_config())
        self.ions_tree.heading('type',
                               text=localization_manager.tr("icv_solv_col_type"),
                               **AppStyles.treeview_headings_config())
        self.ions_tree.column('name', width=100)
        self.ions_tree.column('type', width=100)

        ions_scroll = ttk.Scrollbar(ions_frame, orient=tk.VERTICAL, command=self.ions_tree.yview)
        self.ions_tree.configure(yscrollcommand=ions_scroll.set)

        self.ions_tree.grid(row=0, column=0, sticky="nsew")
        ions_scroll.grid(row=0, column=1, sticky="ns")

        right_frame = tk.Frame(main_frame, **AppStyles.frame_style(), width=300)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=100)  # Дерево радиусов
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_rowconfigure(2, weight=50)
        right_frame.grid_rowconfigure(3, weight=50)

        radii_frame = tk.LabelFrame(right_frame,
                                    text = localization_manager.tr("icv_radii_frame"),
                                    **AppStyles.labelframe_style())
        radii_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        radii_frame.grid_columnconfigure(0, weight=1)
        radii_frame.grid_rowconfigure(0, weight=1)

        self.radii_tree = ttk.Treeview(
            radii_frame,
            columns=('charge', 'CN', 'radius'),
            show='headings',
            **AppStyles.treeview_config()
        )

        self.radii_tree.heading('charge',
                                text=localization_manager.tr("icv_rad_col_charge"),
                                **AppStyles.treeview_headings_config())
        self.radii_tree.heading('CN',
                                text=localization_manager.tr("icv_rad_col_CN"),
                                **AppStyles.treeview_headings_config())
        self.radii_tree.heading('radius',
                                text=localization_manager.tr("icv_rad_col_radius"),
                                **AppStyles.treeview_headings_config())
        self.radii_tree.column('charge', width=80, anchor=tk.CENTER)
        self.radii_tree.column('CN', width=80, anchor=tk.CENTER)
        self.radii_tree.column('radius', width=120, anchor=tk.CENTER)

        radii_scroll = ttk.Scrollbar(radii_frame, orient=tk.VERTICAL, command=self.radii_tree.yview)
        self.radii_tree.configure(yscrollcommand=radii_scroll.set)

        self.radii_tree.grid(row=0, column=0, sticky="nsew")
        radii_scroll.grid(row=0, column=1, sticky="ns")

        tk.Button(right_frame,
                  text=localization_manager.tr("icv_delete_button"),
                  **AppStyles.button_style(),
                  command=self.controller.delete_selected).grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        form_frame = tk.LabelFrame(right_frame,
                                   text=localization_manager.tr("icv_form_frame"),
                                   **AppStyles.labelframe_style())
        form_frame.grid(row=2, column=0, sticky="nsew", pady=(5, 0))
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
        form_frame.grid_columnconfigure(4, weight=1)

        tk.Label(form_frame,
                 text=localization_manager.tr("icv_ion_form_label_name"),
                 **AppStyles.label_style()).grid(row=0, column=0, sticky="ew", padx=5)
        self.entry_name = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0, sticky="ew", padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("icv_ion_form_label_it"),
                 **AppStyles.label_style()).grid(row=0, column=1, sticky="ew", padx=5)
        self.box_ion_type = ttk.Combobox(form_frame,
                                         values=[localization_manager.tr("icv_ion_form_cb_cat"),
                                                 localization_manager.tr("icv_ion_form_cb_an")],
                                         **AppStyles.combobox_config())
        self.box_ion_type.current(0)
        self.box_ion_type.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("icv_ion_form_label_form"),
                 **AppStyles.label_style()).grid(row=0, column=2, sticky="ew", padx=5)
        self.entry_formula = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_formula.grid(row=1, column=2, sticky="ew", padx=5, pady=2)

        tk.Label(form_frame,
                 text=localization_manager.tr("icv_ion_form_label_val"),
                 **AppStyles.label_style()).grid(row=0, column=3, sticky="ew", padx=5)
        self.entry_valence = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_valence.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        tk.Button(form_frame,
                  text=localization_manager.tr("icv_add_button"),
                  **AppStyles.button_style(),
                  command=self.on_submit).grid(row=1, column=4, sticky="ew", padx=5, pady=2)

        ion_frame = tk.LabelFrame(right_frame,
                                  text=localization_manager.tr("icv_add_rad_frame"),
                                  **AppStyles.labelframe_style())
        ion_frame.grid(row=3, column=0, sticky="nsew", pady=(5, 0))
        ion_frame.grid_columnconfigure(0, weight=1)
        ion_frame.grid_columnconfigure(1, weight=1)
        ion_frame.grid_columnconfigure(2, weight=1)
        ion_frame.grid_columnconfigure(3, weight=1)
        ion_frame.grid_columnconfigure(4, weight=1)
        ion_frame.grid_columnconfigure(5, weight=1)

        tk.Label(ion_frame,
                 text=localization_manager.tr("icv_ion_rad_form_label_name"),
                 **AppStyles.label_style()).grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        self.entry_ion_name = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_ion_name.grid(row=1, column=0, sticky="ew", padx=5, pady=2)
        tk.Label(ion_frame,
                 text=localization_manager.tr("icv_ion_rad_form_label_it"),
                 **AppStyles.label_style()).grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        self.ion_box = ttk.Combobox(ion_frame,
                                    values=[localization_manager.tr("icv_ion_form_cb_cat"),
                                            localization_manager.tr("icv_ion_form_cb_an")],
                                    **AppStyles.combobox_config())
        self.ion_box.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.ion_box.current(0)
        tk.Label(ion_frame,
                 text=localization_manager.tr("icv_ion_rad_form_label_charge"),
                 **AppStyles.label_style()).grid(row=0, column=2, sticky="ew", padx=5, pady=2)
        self.entry_charge = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_charge.grid(row=1, column=2, sticky="ew", padx=5, pady=2)
        tk.Label(ion_frame,
                 text=localization_manager.tr("icv_ion_rad_form_label_cn"),
                 **AppStyles.label_style()).grid(row=0, column=3, sticky="ew", padx=5, pady=2)
        self.entry_CN = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_CN.grid(row=1, column=3, sticky="ew", padx=5, pady=2)
        tk.Label(ion_frame,
                 text=localization_manager.tr("icv_ion_rad_form_label_ir"),
                 **AppStyles.label_style()).grid(row=0, column=4, sticky="ew", padx=5, pady=2)
        self.entry_ionic_radii = tk.Entry(ion_frame, **AppStyles.entry_style())
        self.entry_ionic_radii.grid(row=1, column=4, sticky="ew", padx=5, pady=2)

        tk.Button(ion_frame,
                  text=localization_manager.tr("icv_add_rad_button"),
                  **AppStyles.button_style(),
                  command=self.ion_on_submit).grid(row=1, column=5, sticky="ew", padx=5, pady=2)

    def ion_on_submit(self):
        ion_type = ""
        if self.ion_box.get() == "Анион" or "Anion":
            ion_type = "anion"
        if self.ion_box.get() == "Катион" or "Cation":
            ion_type = "cation"
        ion_data = {
            'name': self.entry_ion_name.get(),
            'ion_type': ion_type,
            'charge': self.entry_charge.get(),
            'CN': self.entry_CN.get(),
            'ionic_radii': self.entry_ionic_radii.get()
        }
        self.controller.ion_handle_submit(ion_data)
        self.ion_clear_form()

    def ion_clear_form(self):
        self.entry_ion_name.delete(0, tk.END)
        self.ion_box.delete(0, tk.END)
        self.entry_charge.delete(0, tk.END)
        self.entry_CN.delete(0, tk.END)
        self.entry_ionic_radii.delete(0, tk.END)

    def on_submit(self):
        ion_type = ""
        if self.box_ion_type.get() == "Анион" or "Anion":
            ion_type = "anion"
        elif self.box_ion_type.get() == "Катион" or "Cation":
            ion_type = "cation"

        data = {
            'name': self.entry_name.get(),
            'ion_type': ion_type,
            'formula': self.entry_formula.get(),
            'valence': self.entry_valence.get()
        }
        self.controller.handle_submit(data)
        self.clear_form()

    def show_ions(self, ions):
        self.ions_tree.delete(*self.ions_tree.get_children())
        for ion in ions:
            self.ions_tree.insert('', 'end', values=(ion['name'], ion['type']))

    def show_radii(self, radii):
        self.radii_tree.delete(*self.radii_tree.get_children())
        for radius in radii:
            self.radii_tree.insert('', 'end', values=(
                radius['charge'],
                radius['CN'],
                f"{radius['ionic_radii']:.3f}"
            ))

    def bind_ion_selection(self, callback):
        self.ions_tree.bind('<<TreeviewSelect>>', callback)

    def get_selected_ion(self):
        selected = self.ions_tree.selection()
        if not selected:
            return None
        item = self.ions_tree.item(selected[0])
        return item['values'][0], item['values'][1]

    def get_selected_radii(self):
        selected = self.radii_tree.selection()
        if not selected:
            return None
        item = self.radii_tree.item(selected[0])
        return item['values'][0], item['values'][1], item['values'][2]

    def show_data(self, data):
        for item in self.ions_tree.get_children():
            self.ions_tree.delete(item)
        for row in data:
            self.ions_tree.insert('', 'end', values=row)

    def show_message(self, title, message):
        mb.showinfo(title, message)

    def show_warning(self, title, message):
        mb.showwarning(title, message)

    def show_error(self, title, message):
        mb.showerror(title, message)

    def ask_confirmation(self, title, message):
        return mb.askyesno(title, message)

    def show_success(self, message):
        mb.showinfo(title="success", message=message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_formula.delete(0, tk.END)
        self.entry_valence.delete(0, tk.END)