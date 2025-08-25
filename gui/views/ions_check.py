import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from gui.default_style import AppStyles

class IonsCheckView(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ионные радиусы")
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.geometry("800x600")
        self.styles = AppStyles()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self, **AppStyles.frame_style())
        main_frame.pack(fill=BOTH, expand=True)

        ions_frame = LabelFrame(main_frame, text="Ионы", **AppStyles.labelframe_style())
        ions_frame.pack(side=LEFT, fill=Y)

        self.ions_tree = ttk.Treeview(
            ions_frame,
            columns=('name', 'type'),
            show='headings',
            height=20,
            **AppStyles.treeview_config()
        )
        self.ions_tree.heading('name', text='Ион', **AppStyles.treeview_headings_config())
        self.ions_tree.heading('type', text='Тип', **AppStyles.treeview_headings_config())
        self.ions_tree.column('name', width=100)
        self.ions_tree.column('type', width=100)

        ions_scroll = ttk.Scrollbar(ions_frame, orient=VERTICAL, command=self.ions_tree.yview)
        self.ions_tree.configure(yscrollcommand=ions_scroll.set)

        self.ions_tree.pack(side=LEFT, fill=BOTH, expand=True)
        ions_scroll.pack(side=RIGHT, fill=Y)

        radii_frame = LabelFrame(main_frame, text="Ионные радиусы", **AppStyles.labelframe_style())
        radii_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        self.radii_tree = ttk.Treeview(
            radii_frame,
            columns=('charge', 'CN', 'radius'),
            show='headings',
            height=20,
            **AppStyles.treeview_config()
        )
        self.radii_tree.heading('charge', text='заряд', **AppStyles.treeview_headings_config())
        self.radii_tree.heading('CN', text='КЧ', **AppStyles.treeview_headings_config())
        self.radii_tree.heading('radius', text='радиус', **AppStyles.treeview_headings_config())
        self.radii_tree.column('charge', width=80, anchor=CENTER)
        self.radii_tree.column('CN', width=80, anchor=CENTER)
        self.radii_tree.column('radius', width=120, anchor=CENTER)

        radii_scroll = ttk.Scrollbar(radii_frame, orient=VERTICAL, command=self.radii_tree.yview)
        self.radii_tree.configure(yscrollcommand=radii_scroll.set)

        self.radii_tree.pack(side=LEFT, fill=BOTH, expand=True)
        radii_scroll.pack(side=RIGHT, fill=Y)

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
        return item['values'][0], item['values'][1]  # name, type

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)