import tkinter as tk
from tkinter import ttk
from gui.default_style import AppStyles
import tkinter.messagebox as mb


class SolventsCheckView(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=AppStyles.BACKGROUND_COLOR)
        self.styles = AppStyles()
        self.attributes('-fullscreen', True)
        menu = tk.Menu(self)
        menu.add_command(label="Выйти", command=self.destroy)
        self.config(menu=menu)
        self.title("Solvents viewer")

        self.build_ui()

    def build_ui(self):
        self.main_frame = tk.Frame(self, **AppStyles.frame_style())
        self.main_frame.pack(fill="both", expand=True)

        # Создаем основной PanedWindow для разделения на две колонки
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=10, pady=5)

        # ПЕРВАЯ КОЛОНКА (Treeview с прокруткой)
        first_col_frame = tk.Frame(self.paned_window)
        self.paned_window.add(first_col_frame, weight=2)

        # Treeview с прокруткой
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

        # Настройка колонок treeview
        self.tree.heading('name', text='Название')
        self.tree.heading('type', text='Тип')
        self.tree.heading('formula', text='Формула')
        self.tree.heading('density', text='Плотность')
        self.tree.heading('boiling_point', text='Температура кипения')
        self.tree.heading('notes', text='Заметки')

        self.tree.column('name', width=150, anchor='center')
        self.tree.column('type', width=100, anchor='center')
        self.tree.column('formula', width=100, anchor='center')
        self.tree.column('density', width=100, anchor='center')
        self.tree.column('boiling_point', width=150, anchor='center')
        self.tree.column('notes', width=200, anchor='center')

        # Кнопка удаления под treeview
        delete_frame = tk.Frame(first_col_frame)
        delete_frame.pack(fill="x", pady=5)

        delete_btn = tk.Button(delete_frame, text="Удалить выбранное",
                               command=self.controller.delete_selected,
                               **AppStyles.button_style())
        delete_btn.pack(fill="x", padx=10)

        # ВТОРАЯ КОЛОНКА (Форма загрузки)
        second_col_frame = tk.Frame(self.paned_window)
        self.paned_window.add(second_col_frame, weight=1)

        # Фрейм для формы загрузки
        form_frame = tk.LabelFrame(second_col_frame, text="Добавить растворитель",
                                   **AppStyles.labelframe_style())
        form_frame.pack(fill="both", expand=True)
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=1)

        # Поля формы
        tk.Label(form_frame, text="Название", **AppStyles.label_style()).grid(row=0, column=0, sticky='ew', padx=5,
                                                                              pady=2)
        self.entry_name = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_name.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame, text="Тип", **AppStyles.label_style()).grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.box_solvent_type = ttk.Combobox(form_frame, values=["Растворитель", "Антирастворитель"],
                                             **AppStyles.combobox_config())
        self.box_solvent_type.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        self.box_solvent_type.current(0)

        tk.Label(form_frame, text="Формула", **AppStyles.label_style()).grid(row=2, column=0, sticky='ew', padx=5,
                                                                             pady=2)
        self.entry_formula = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_formula.grid(row=3, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame, text="Плотность, г/мл", **AppStyles.label_style()).grid(row=2, column=1, sticky='ew',
                                                                                     padx=5, pady=2)
        self.entry_density = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_density.grid(row=3, column=1, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame, text="Температура кипения, C", **AppStyles.label_style()).grid(row=4, column=0,
                                                                                            sticky='ew', padx=5, pady=2)
        self.entry_bp = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_bp.grid(row=5, column=0, sticky='ew', padx=5, pady=2)

        tk.Label(form_frame, text="Заметки", **AppStyles.label_style()).grid(row=4, column=1, sticky='ew', padx=5,
                                                                             pady=2)
        self.entry_notes = tk.Entry(form_frame, **AppStyles.entry_style())
        self.entry_notes.grid(row=5, column=1, sticky='ew', padx=5, pady=2)

        # Кнопка загрузки под формой
        button_frame = tk.Frame(second_col_frame)
        button_frame.pack(fill="x", pady=5)

        upload_btn = tk.Button(button_frame, text="Загрузить данные",
                               command=self.on_submit,
                               **AppStyles.button_style())
        upload_btn.pack(fill="x", padx=5)

    def on_submit(self):
        type = ""
        if self.box_solvent_type.get() == "Растворитель":
            type = "solvent"
        elif self.box_solvent_type.get() == "Антирастворитель":
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

    def show_success(self, message):
        mb.showinfo(title="success", message=message)
        self.clear_form()

    def show_error(self, message):
        mb.showerror(title="error", message=message)

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.box_solvent_type.set('Растворитель')
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

    def show_message(self, title, message):
        mb.showinfo(title, message)

    def show_warning(self, title, message):
        mb.showwarning(title, message)

    def show_error(self, title, message):
        mb.showerror(title, message)

    def ask_confirmation(self, title, message):
        return mb.askyesno(title, message)