import tkinter as tk
from tkinter import ttk
from gui.default_style import AppStyles

class TemplateView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title("Add new phase template")
        self.wm_attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)
        self.build_ui()
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.site_frames = []

    def build_ui(self):

        info_frame = tk.LabelFrame(self, text="Шаблоны перовскитов",
                                   **AppStyles.labelframe_style())
        info_frame.grid(row=0, column=0, columnspan=4)

        tk.Label(info_frame, text="Название шаблона",
                 **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_name = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0)

        tk.Label(info_frame, text="Размерность",
                 **AppStyles.label_style()).grid(row=0, column=1)
        self.entry_dimensionality = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_dimensionality.grid(row=1, column=1)

        tk.Label(info_frame, text="Описание",
                 **AppStyles.label_style()).grid(row=0, column=2)
        self.entry_description = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_description.grid(row=1, column=2)

        tk.Label(info_frame, text="Стехиометрия аниона",
                 **AppStyles.label_style()).grid(row=0, column=3)
        self.entry_anion_stoich = tk.Entry(info_frame, **AppStyles.entry_style())
        self.entry_anion_stoich.grid(row=1, column=3)

        sites_frame = tk.Frame(self, **AppStyles.frame_style())
        sites_frame.grid(row=1, column=0, columnspan=4)

        tk.Label(sites_frame, text="Выберите типы катионов:",
                 **AppStyles.label_style()).pack()

        self.site_vars = {
            'a_site': tk.IntVar(),
            'b_site': tk.IntVar(),
            'b_double': tk.IntVar(),
            'spacer': tk.IntVar()
        }

        tk.Checkbutton(sites_frame, text="A-катион",
                        variable=self.site_vars['a_site'],
                        **AppStyles.checkbutton_style()).pack(side='left', padx=5)
        tk.Checkbutton(sites_frame, text="B-катион",
                       variable=self.site_vars['b_site'],
                        **AppStyles.checkbutton_style()).pack(side='left', padx=5)
        tk.Checkbutton(sites_frame, text="B-катион (двойной)",
                       variable=self.site_vars['b_double'],
                        **AppStyles.checkbutton_style()).pack(side='left', padx=5)
        tk.Checkbutton(sites_frame, text="Спейсер",
                       variable=self.site_vars['spacer'],
                        **AppStyles.checkbutton_style()).pack(side='left', padx=5)

        button_frame = tk.Frame(self, **AppStyles.frame_style())
        button_frame.grid(row=2, column=0, columnspan=4)

        self.btn_add_sites = tk.Button(button_frame, text="Добавить элементы структуры",
                                       command=self.on_add_sites)
        self.btn_add_sites.pack(side='left', padx=5)

        self.btn_submit = tk.Button(button_frame, text="Подтвердить шаблон",
                                    command=self.on_submit_template)
        self.btn_submit.pack(side='left', padx=5)
        self.btn_submit.config(state='disabled')

    def create_site_frames(self):
        for frame in self.site_frames:
            frame.destroy()
        self.site_frames = []
        row = 3
        for site_type, var in self.site_vars.items():
            if var.get():
                frame = SiteFrame(self, site_type.replace('_', ' ').title())
                frame.grid(row=row, column=0, columnspan=4, sticky="ew", padx=20, pady=5)
                self.site_frames.append(frame)
                row += 1

        if self.site_frames:
            self.btn_submit.config(state='normal')

    def on_add_sites(self):

        self.controller.handle_add_sites({
            'name': self.entry_name.get(),
            'dimensionality': self.entry_dimensionality.get(),
            'description': self.entry_description.get(),
            'anion_stoich': self.entry_anion_stoich.get(),
            'site_types': {k: v.get() for k, v in self.site_vars.items()}
        })

    def on_submit_template(self):

        site_data = []
        for frame in self.site_frames:
            data = frame.get_data()
            if data:
                site_data.append({
                    'type': frame.site_type.lower().replace(' ', '_'),
                    'stoichiometry': data[0],
                    'valence': data[1]
                })

        self.controller.handle_submit_template(site_data)

    def show_success(self, message):
        tk.messagebox.showinfo("Success", message)
        self.clear_form()

    def show_error(self, message):
        tk.messagebox.showerror("Error", message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_dimensionality.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.entry_anion_stoich.delete(0, tk.END)

        for var in self.site_vars.values():
            var.set(0)

        for frame in self.site_frames:
            frame.destroy()
        self.site_frames = []

        self.btn_submit.config(state='disabled')


class SiteFrame(tk.LabelFrame):
    def __init__(self, parent, site_type):
        super().__init__(parent, text=site_type)
        self.site_type = site_type

        tk.Label(self, text="Базовая стехиометрия",
                 **AppStyles.label_style()).grid(row=0, column=0)
        self.entry_stoich = tk.Entry(self, **AppStyles.entry_style())
        self.entry_stoich.grid(row=1, column=0)

        tk.Label(self, text="Базовая валентность",
                 **AppStyles.label_style()).grid(row=0, column=1)
        self.entry_valence = tk.Entry(self, **AppStyles.entry_style())
        self.entry_valence.grid(row=1, column=1)

    def get_data(self):
        stoich = self.entry_stoich.get()
        valence = self.entry_valence.get()

        if not all([stoich, valence]):
            return None

        return stoich, valence