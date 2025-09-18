import tkinter as tk
from tkinter import ttk, messagebox
from gui.default_style import AppStyles

class TemplatesCheckView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Управление шаблонами перовскитов")
        self.attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.site_frames = []

        self.build_ui()

    def bind_template_selection(self, callback):
        self.temp_tree.bind('<<TreeviewSelect>>', callback)

    def build_ui(self):
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_paned, **AppStyles.frame_style())
        main_paned.add(left_frame)

        right_frame = tk.Frame(main_paned, **AppStyles.frame_style(), width=150)
        main_paned.add(right_frame)

        main_paned.pane(left_frame, weight=1)
        main_paned.pane(right_frame, weight=0)

        temp_frame = tk.LabelFrame(left_frame, text="Существующие шаблоны",
                                   **AppStyles.labelframe_style())
        temp_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tree_container = tk.Frame(temp_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)

        self.temp_tree = ttk.Treeview(
            tree_container,
            columns=('id', 'name', 'anion_stoichiometry', 'dimensionality', 'description'),
            show='headings',
            height=15
        )
        self.temp_tree.heading('id', text='ID')
        self.temp_tree.heading('name', text='Имя')
        self.temp_tree.heading('anion_stoichiometry', text='Стехиометрия аниона')
        self.temp_tree.heading('dimensionality', text='Размерность')
        self.temp_tree.heading('description', text='Описание')

        for col in ('id', 'name', 'anion_stoichiometry', 'dimensionality', 'description'):
            self.temp_tree.column(col, width=100, anchor=tk.CENTER)

        temp_scroll_vertical = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.temp_tree.yview)
        self.temp_tree.configure(yscrollcommand=temp_scroll_vertical.set)

        temp_scroll_horizontal = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.temp_tree.xview)
        self.temp_tree.configure(xscrollcommand=temp_scroll_horizontal.set)

        self.temp_tree.grid(row=0, column=0, sticky='nsew')
        temp_scroll_vertical.grid(row=0, column=1, sticky='ns')
        temp_scroll_horizontal.grid(row=1, column=0, sticky='ew')

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        button_frame_left = tk.Frame(left_frame, **AppStyles.frame_style())
        button_frame_left.pack(fill=tk.X, padx=5, pady=2)

        delete_btn = tk.Button(button_frame_left, text="Удалить выбранное",
                               command=self.controller.delete_selected,
                               **AppStyles.button_style())
        delete_btn.pack(side="left", fill="x", padx=5, expand=True)

        details_frame = tk.LabelFrame(right_frame, text="Детали выбранного шаблона",
                                      **AppStyles.labelframe_style())
        details_frame.pack(fill=tk.X, padx=5, pady=2)

        self.sites_tree = ttk.Treeview(
            details_frame,
            columns=('type', 'stoichiometry', 'valence'),
            show='headings',
            height=10,
            **AppStyles.treeview_config()
        )
        self.sites_tree.heading('type', text='Тип')
        self.sites_tree.heading('stoichiometry', text='Стехиометрия')
        self.sites_tree.heading('valence', text='Валентность')

        for col in ('type', 'stoichiometry', 'valence'):
            self.sites_tree.column(col, width=100, anchor=tk.CENTER)

        sites_scroll = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.sites_tree.yview)
        self.sites_tree.configure(yscrollcommand=sites_scroll.set)

        self.sites_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sites_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.temp_tree.bind('<<TreeviewSelect>>', self.on_template_select)

        form_container = tk.Frame(right_frame, **AppStyles.frame_style())
        form_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        form_frame = tk.LabelFrame(form_container, text="Добавить новый шаблон",
                                   **AppStyles.labelframe_style())
        form_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(form_frame, bg=AppStyles.BACKGROUND_COLOR)
        scrollbar = ttk.Scrollbar(form_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, **AppStyles.frame_style())

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.site_vars = {
            'a_site': tk.IntVar(),
            'b_site': tk.IntVar(),
            'b_double': tk.IntVar(),
            'spacer': tk.IntVar()
        }
        scrollable_frame = tk.Frame(form_frame, **AppStyles.frame_style())
        scrollable_frame.pack(fill=tk.BOTH, expand=True)

        # Настраиваем grid для управления шириной
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)
        scrollable_frame.columnconfigure(2, weight=1)
        scrollable_frame.columnconfigure(3, weight=1)

        info_frame = tk.Frame(scrollable_frame, **AppStyles.frame_style())
        info_frame.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=2)

        # Настраиваем колонки info_frame для равномерного распределения
        for i in range(4):
            info_frame.columnconfigure(i, weight=1, uniform="group1")

        tk.Label(info_frame, text="Название шаблона",
                 **AppStyles.label_style()).grid(row=0, column=0, sticky='ew', padx=5, pady=2)
        self.entry_name = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(info_frame, text="Размерность",
                 **AppStyles.label_style()).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.entry_dimensionality = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_dimensionality.grid(row=1, column=1, sticky='ew', padx=5, pady=2)

        tk.Label(info_frame, text="Описание",
                 **AppStyles.label_style()).grid(row=0, column=2, sticky='ew', padx=5, pady=2)
        self.entry_description = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_description.grid(row=1, column=2, sticky='ew', padx=5, pady=2)

        tk.Label(info_frame, text="Стехиометрия аниона",
                 **AppStyles.label_style()).grid(row=0, column=3, sticky='ew', padx=5, pady=2)
        self.entry_anion_stoich = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_anion_stoich.grid(row=1, column=3, sticky='ew', padx=5, pady=2)

        # Остальные элементы также размещаем с sticky='ew' для растягивания
        tk.Label(scrollable_frame, text="Выберите типы катионов:",
                 **AppStyles.label_style()).grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=2)

        check_frame = tk.Frame(scrollable_frame, **AppStyles.frame_style())
        check_frame.grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=2)

        # Настраиваем check_frame для равномерного распределения
        for i in range(4):
            check_frame.columnconfigure(i, weight=1, uniform="group2")

        tk.Checkbutton(check_frame, text="A-катион",
                       variable=self.site_vars['a_site'],
                       **AppStyles.checkbutton_style()).grid(row=0, column=0, sticky='ew', padx=5)
        tk.Checkbutton(check_frame, text="B-катион",
                       variable=self.site_vars['b_site'],
                       **AppStyles.checkbutton_style()).grid(row=0, column=1, sticky='ew', padx=5)
        tk.Checkbutton(check_frame, text="B-катион (двойной)",
                       variable=self.site_vars['b_double'],
                       **AppStyles.checkbutton_style()).grid(row=0, column=2, sticky='ew', padx=5)
        tk.Checkbutton(check_frame, text="Спейсер",
                       variable=self.site_vars['spacer'],
                       **AppStyles.checkbutton_style()).grid(row=0, column=3, sticky='ew', padx=5)

        button_frame_form = tk.Frame(scrollable_frame, **AppStyles.frame_style())
        button_frame_form.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=2)

        # Настраиваем button_frame_form для равномерного распределения
        button_frame_form.columnconfigure(0, weight=1)
        button_frame_form.columnconfigure(1, weight=1)

        self.btn_add_sites = tk.Button(button_frame_form, text="Добавить элементы структуры",
                                       command=self.on_add_sites,
                                       **AppStyles.button_style())
        self.btn_add_sites.grid(row=0, column=0, sticky='ew', padx=5)

        self.btn_submit = tk.Button(button_frame_form, text="Подтвердить шаблон",
                                    command=self.on_submit_template,
                                    **AppStyles.button_style())
        self.btn_submit.grid(row=0, column=1, sticky='ew', padx=5)
        self.btn_submit.config(state='disabled')

        self.sites_container = tk.Frame(scrollable_frame, **AppStyles.frame_style())
        self.sites_container.grid(row=4, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

        # Важно: настраиваем веса для scrollable_frame
        scrollable_frame.rowconfigure(4, weight=1)  # sites_container будет растягиваться
        for i in range(4):
            scrollable_frame.columnconfigure(i, weight=1)

        # Обновляем геометрию при изменении содержимого
        def update_right_frame_width():
            right_frame.update_idletasks()
            width = scrollable_frame.winfo_reqwidth() + 20  # + отступы
            main_paned.paneconfigure(right_frame, width=width)

        # Привязываем обновление ширины к изменениям
        scrollable_frame.bind("<Configure>", lambda e: update_right_frame_width())

    def on_add_sites(self):
        self.controller.handle_add_sites({
            'name': self.entry_name.get(),
            'dimensionality': self.entry_dimensionality.get(),
            'description': self.entry_description.get(),
            'anion_stoich': self.entry_anion_stoich.get(),
            'site_types': {k: v.get() for k, v in self.site_vars.items()}
        })
        self.btn_add_sites.config(state = 'disabled')

    def create_site_frames(self):
        for widget in self.sites_container.winfo_children():
            widget.destroy()
        self.site_frames = []

        for site_type, var in self.site_vars.items():
            if var.get():
                frame = SiteFrame(self.sites_container, site_type.replace('_', ' ').title())
                frame.pack(fill=tk.X, padx=5, pady=2)
                self.site_frames.append(frame)

        if self.site_frames:
            self.btn_submit.config(state='normal')

    def on_submit_template(self):
        site_data = []
        for frame in self.site_frames:
            data = frame.get_data()
            if data:
                site_dict = {
                    'type': frame.site_type.lower().replace(' ', '_'),
                    'stoichiometry': data[0],
                    'valence': data[1]
                }
                site_data.append(site_dict)

        self.controller.handle_submit_template(site_data)

    def on_template_select(self, event):
        selected = self.temp_tree.selection()
        if selected:
            item = self.temp_tree.item(selected[0])
            template_id = item['values'][0]
            self.controller.load_template_details(template_id)

    def show_template(self, templates):
        self.temp_tree.delete(*self.temp_tree.get_children())
        for template in templates:
            self.temp_tree.insert('', 'end', values=(
                template['id'], template['name'],
                template['anion_stoichiometry'],
                template['dimensionality'], template['description']
            ))

    def show_sites(self, sites):
        self.sites_tree.delete(*self.sites_tree.get_children())
        for site in sites:
            self.sites_tree.insert('', 'end', values=(
                site['type'],
                site['stoichiometry'],
                site['valence']
            ))

    def get_selected_template(self):
        selected = self.temp_tree.selection()
        if not selected:
            return None
        item = self.temp_tree.item(selected[0])
        return (item['values'][0], item['values'][1], item['values'][2],
                item['values'][3], item['values'][4])

    def show_message(self, title, message):
        tk.messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        tk.messagebox.showwarning(title, message)

    def show_error(self, title, message):
        tk.messagebox.showerror(title, message)

    def ask_confirmation(self, title, message):
        return tk.messagebox.askyesno(title, message)

    def show_success(self, message):
        self.show_message("Success", message)
        self.clear_form()

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_dimensionality.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.entry_anion_stoich.delete(0, tk.END)

        for var in self.site_vars.values():
            var.set(0)

        for widget in self.sites_container.winfo_children():
            widget.destroy()
        self.site_frames = []

        self.btn_submit.config(state='disabled')
        self.sites_tree.delete(*self.sites_tree.get_children())

class SiteFrame(tk.LabelFrame):
    def __init__(self, parent, site_type):
        super().__init__(parent, text=site_type, **AppStyles.labelframe_style())
        self.site_type = site_type

        tk.Label(self, text="Базовая стехиометрия",
                 **AppStyles.label_style()).grid(row=0, column=0, sticky = 'ew', padx=5, pady=2)
        self.entry_stoich = tk.Entry(self, **AppStyles.entry_style())
        self.entry_stoich.grid(row=1, column=0, sticky = 'ew', padx=5, pady=2)

        tk.Label(self, text="Базовая валентность",
                 **AppStyles.label_style()).grid(row=0, column=1, sticky = 'ew', padx=5, pady=2)
        self.entry_valence = tk.Entry(self, **AppStyles.entry_style())
        self.entry_valence.grid(row=1, column=1, sticky = 'ew', padx=5, pady=2)

    def get_data(self):
        stoich = self.entry_stoich.get()
        valence = self.entry_valence.get()

        if not all([stoich, valence]):
            return None

        return stoich, valence