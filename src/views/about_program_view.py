from src.default_style import AppStyles
import tkinter as tk
from tkinter import ttk, scrolledtext
from src.language.manager import localization_manager

class AboutProgramView(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        localization_manager.register_observer(self)
        self.title(localization_manager.tr("about_window_title"))
        self.configure(bg=AppStyles.BACKGROUND_COLOR)

        self.help_content = self._get_help_content()

        self._build_ui()
        self._setup_and_center_window()
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

    def _setup_and_center_window(self):
        """
        Рассчитывает оптимальный размер окна на основе размера экрана
        и центрирует его.
        """
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width_ratio = 0.8
        window_height_ratio = 0.85
        window_width = int(screen_width * window_width_ratio)
        window_height = int(screen_height * window_height_ratio)
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
        self.minsize(600, 400)

    def _get_help_content(self):
        return {
            "root": "help_root",
            "workflow": "help_workflow",
            "workflow_template": "help_workflow_template",
            "workflow_structure": "help_workflow_structure",
            "workflow_solution": "help_workflow_solution",
            "workflow_kfactors": "help_workflow_kfactors",
            "workflow_results": "help_workflow_results",
            "workflow_sorting": "help_workflow_sorting",
            "workflow_saving": "help_workflow_saving",
            "data": "help_data",
            "data_compositions": "help_data_compositions",
            "data_templates": "help_data_templates",
            "data_ions": "help_data_ions",
            "data_solvents": "help_data_solvents",
            "about": "help_about",
            "about_purpose": "help_about_purpose",
            "about_cite": "help_about_cite",
            "about_license": "help_about_license",
            "about_acknowledgements": "help_about_acknowledgements",
        }

    def _build_ui(self):
        """Создает основные элементы пользовательского интерфейса окна."""
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_frame = ttk.Frame(paned_window, padding=5)
        self.tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        paned_window.add(tree_frame, weight=1)

        text_frame = ttk.Frame(paned_window, padding=5)
        self.text_display = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, font=("Helvetica", 11), padx=5, pady=5
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        self.text_display.config(state="disabled")
        paned_window.add(text_frame, weight=3)

        self._populate_tree()
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        self.tree.selection_set("root")
        self._on_tree_select(None)

    def _populate_tree(self):

        self.tree.insert('', 'end', iid='root',
                         text=localization_manager.tr('tree_welcome'), open=True)
        workflow = self.tree.insert('', 'end', iid='workflow',
                                    text=localization_manager.tr('tree_workflow'), open=True)
        data = self.tree.insert('', 'end', iid='data',
                                text=localization_manager.tr('tree_data'), open=True)
        about = self.tree.insert('', 'end', iid='about',
                                 text=localization_manager.tr('tree_about'), open=True)

        self.tree.insert(workflow, 'end', iid='workflow_template',
                         text=localization_manager.tr('tree_workflow_template'))
        self.tree.insert(workflow, 'end', iid='workflow_structure',
                         text=localization_manager.tr('tree_workflow_structure'))
        self.tree.insert(workflow, 'end', iid='workflow_solution',
                         text=localization_manager.tr('tree_workflow_solution'))
        self.tree.insert(workflow, 'end', iid='workflow_kfactors',
                         text=localization_manager.tr('tree_workflow_kfactors'))
        self.tree.insert(workflow, 'end', iid='workflow_results',
                         text=localization_manager.tr('tree_workflow_results'))
        self.tree.insert(workflow, 'end', iid='workflow_sorting',
                         text=localization_manager.tr('tree_workflow_sorting'))
        self.tree.insert(workflow, 'end', iid='workflow_saving',
                         text=localization_manager.tr('tree_workflow_saving'))

        self.tree.insert(data, 'end', iid='data_compositions',
                         text=localization_manager.tr('tree_data_compositions'))
        self.tree.insert(data, 'end', iid='data_templates',
                         text=localization_manager.tr('tree_data_templates'))
        self.tree.insert(data, 'end', iid='data_ions',
                         text=localization_manager.tr('tree_data_ions'))
        self.tree.insert(data, 'end', iid='data_solvents',
                         text=localization_manager.tr('tree_data_solvents'))

        self.tree.insert(about, 'end', iid='about_purpose',
                         text=localization_manager.tr('tree_about_purpose'))
        self.tree.insert(about, 'end', iid='about_cite',
                         text=localization_manager.tr('tree_about_cite'))
        self.tree.insert(about, 'end', iid='about_license',
                         text=localization_manager.tr('tree_about_license'))
        self.tree.insert(about, 'end', iid='about_acknowledgements',
                         text=localization_manager.tr('tree_about_acknowledgements'))

    def _on_tree_select(self, event):
        """
        Функция обратного вызова, срабатывающая при выборе элемента в древовидном списке.
        Она обновляет текстовое поле соответствующим локализованным содержимым.
        """
        if not self.tree.selection():
            return

        selected_item_id = self.tree.selection()[0]

        localization_key = self.help_content.get(selected_item_id, "help_not_found")

        content = localization_manager.tr(localization_key)

        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", content)
        self.text_display.config(state="disabled")