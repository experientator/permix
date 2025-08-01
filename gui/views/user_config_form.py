import tkinter as tk
from tkinter import ttk
from analysis import get_templates_list, get_template_id, get_template_sites, get_candidate_cations

get_template_id()
from gui.controllers.phase_template_form import TemplateController


class UserConfigView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Main calculator")
        self.build_ui()
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
        TemplateController(self)

    def create_template_frame(self):
        info_frame = tk.LabelFrame(self.first_column, text="Выбор шаблона")
        info_frame.pack(fill='x', pady=5)

        tk.Label(info_frame, text="Шаблон фазы").pack(fill='x', pady=5)
        self.phase_template = ttk.Combobox(info_frame, values=get_templates_list())
        self.phase_template.pack(fill='x', pady=5)

        tk.Button(info_frame, text="Просмотр шаблонов", command = self.open_template_form).grid(row=0, column=0)
        tk.Button(info_frame, text="Подтвердить", command=self.create_sites).grid(row=0, column=1)

    def create_sites(self):
        self.sites_frame = tk.LabelFrame(self.first_column, text="Структура")
        self.sites_frame.pack(fill='x', pady=5)

        template_id = get_template_id(self.phase_template.get())
        sites_data = get_template_sites(template_id)
        values_sites = ["1","2","3","4"]
        for index, sites_row in sites_data.iterrows():
            self.site_num = ttk.Combobox(self.sites_frame, values=values_sites, state="readonly")
            self.site_num.current(1)
            self.site_num.pack(fill='x', pady=5)
            self.create_dynamic_site(sites_row, self.site_num.get())
            tk.Label(self.sites_frame, text = "катион").grid(row=0, column=1)
            tk.Label(self.sites_frame,text="количество").grid(row=0, column=2)
    def create_dynamic_site(self, sites_row, site_num):
        for i in range(site_num):
            cations = get_candidate_cations(sites_row["name_candidates"])
            tk.Label(self.sites_frame, text=f"{sites_row["type"]}").grid(row=i+1, column=0)
            self.cb_site_cation = ttk.Combobox(self.sites_frame, values=cations)
            self.cb_site_cation.grid(row=i+1, column=1)

            self.entry_site_fraction = tk.Entry(self.sites_frame)
            self.entry_site_fraction.grid(row=i+1, column=2)
