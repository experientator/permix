import tkinter
from tkinter import *
from tkinter import ttk, messagebox
from gui.default_style import AppStyles

class TemplatesCheckView(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Шаблоны")
        self.wm_attributes('-fullscreen', True)
        menu = Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self,
                 **AppStyles.frame_style())
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        temp_frame = LabelFrame(main_frame, text="Шаблоны",
                 **AppStyles.labelframe_style())
        temp_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)

        self.temp_tree = ttk.Treeview(
            temp_frame,
            columns=('id', 'name', 'anion_stoichiometry', 'dimensionality', 'description'),
            show='headings',
            height=20
        )
        self.temp_tree.heading('id', text='id')
        self.temp_tree.heading('name', text='имя')
        self.temp_tree.heading('anion_stoichiometry', text='стехиометрия аниона')
        self.temp_tree.heading('dimensionality', text='размерность')
        self.temp_tree.heading('description', text='описание')
        self.temp_tree.column('id', width=100)
        self.temp_tree.column('name', width=100)
        self.temp_tree.column('anion_stoichiometry', width=100)
        self.temp_tree.column('dimensionality', width=100)
        self.temp_tree.column('description', width=100)

        temp_scroll = ttk.Scrollbar(temp_frame, orient=VERTICAL, command=self.temp_tree.yview)
        self.temp_tree.configure(yscrollcommand=temp_scroll.set)

        self.temp_tree.pack(side=LEFT, fill=BOTH, expand=True)
        temp_scroll.pack(side=RIGHT, fill=Y)

        sites_frame = LabelFrame(main_frame, text="структура",
                 **AppStyles.labelframe_style())
        sites_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.sites_tree = ttk.Treeview(
            sites_frame,
            columns=('type', 'stoichiometry', 'valence'),
            show='headings',
            height=20,
            **AppStyles.treeview_config()
        )
        self.sites_tree.heading('type', text='тип')
        self.sites_tree.heading('stoichiometry', text='стехиометрия')
        self.sites_tree.heading('valence', text='валентность')
        self.sites_tree.column('type', width=80, anchor=CENTER)
        self.sites_tree.column('stoichiometry', width=80, anchor=CENTER)
        self.sites_tree.column('valence', width=120, anchor=CENTER)

        sites_scroll = ttk.Scrollbar(sites_frame, orient=VERTICAL, command=self.sites_tree.yview)
        self.sites_tree.configure(yscrollcommand=sites_scroll.set)

        self.sites_tree.pack(side=LEFT, fill=BOTH, expand=True)
        sites_scroll.pack(side=RIGHT, fill=Y)

    def show_template(self, templates):
        self.temp_tree.delete(*self.temp_tree.get_children())
        for template in templates:
            self.temp_tree.insert('', 'end', values=(template['id'], template['name'],
                                                     template['anion_stoichiometry'],
                                                     template['dimensionality'], template['description']))

    def show_sites(self, sites):
        self.sites_tree.delete(*self.sites_tree.get_children())
        for site in sites:
            self.sites_tree.insert('', 'end', values=(
                site['type'],
                site['stoichiometry'],
                site['valence']
            ))

    def bind_template_selection(self, callback):
        self.temp_tree.bind('<<TreeviewSelect>>', callback)

    def get_selected_template(self):
        selected = self.temp_tree.selection()
        if not selected:
            return None
        item = self.temp_tree.item(selected[0])
        return (item['values'][0], item['values'][1], item['values'][2],
                item['values'][3], item['values'][4])

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)