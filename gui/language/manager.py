from gui.language.database import LocalizationDB


class LocalizationManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.db = LocalizationDB()
            self.current_language = 'ru'
            self.translations = {}
            self.observers = []  # Список окон для обновления при смене языка
            self.load_translations()
            self.initialized = True

    def set_language(self, language: str):
        """Установить текущий язык (ru/en)"""
        if language in ['ru', 'en']:
            self.current_language = language
            self.load_translations()
            self.notify_observers()

    def load_translations(self):
        """Загрузить все переводы для текущего языка"""
        self.translations = self.db.get_all_translations(self.current_language)

    def tr(self, name: str) -> str:
        """Получить перевод по имени"""
        return self.translations.get(name, name)

    def register_observer(self, observer):
        """Зарегистрировать окно для обновления при смене языка"""
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister_observer(self, observer):
        """Удалить окно из списка наблюдателей"""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        """Уведомить все окна о смене языка"""
        for observer in self.observers:
            if hasattr(observer, 'update_language'):
                observer.update_language()

    def initialize_default_translations(self):
        """Инициализировать базовые переводы"""
        default_translations = [
            # Основные надписи интерфейса
            ("window_title_composition_check", "Composition Check", "Просмотр соединений"),
            ("menu_exit", "Exit", "Выйти"),
            ("button_refresh_all", "Refresh All", "Обновить все"),
            ("button_switch_language", "Switch to English", "Переключить на русский"),

            # Фреймы
            ("frame_main_configs", "Main Configurations", "Основные конфигурации"),
            ("frame_favorite_configs", "Favorite Configurations", "Избранные конфигурации"),
            ("frame_details", "Details", "Детали"),

            # Колонки таблиц
            ("col_id", "ID", "ID"),
            ("col_name", "Name", "Название"),
            ("col_doi", "DOI", "DOI"),
            ("col_data_type", "Data Type", "Тип данных"),
            ("col_notes", "Notes", "Заметки"),
            ("col_template", "Template", "Шаблон"),
            ("col_phase_id", "Phase ID", "ID фазы"),
            ("col_phase_template", "Phase Template", "Шаблон фазы"),
            ("col_solution_volume", "Solution Volume", "V раствора"),
            ("col_antisolvent_volume", "Antisolvent Volume", "V антирастворителя"),
            ("col_concentration", "Concentration", "Концентрация"),

            # Вкладки
            ("tab_main", "Main", "Основное"),
            ("tab_solvents", "Solvents", "Растворители"),
            ("tab_structure", "Structure", "Структура"),
            ("tab_properties", "Properties", "Свойства"),
            ("tab_kfactors", "K-Factors", "K-факторы"),

            # Детали
            ("label_solution_concentration", "Solution Concentration", "Концентрация раствора"),
            ("label_phase_template", "Phase Template ID", "ID шаблона"),
            ("label_band_gap", "Band Gap", "Ширина запрещенной зоны"),
            ("label_stability_notes", "Stability Notes", "Заметки стабильности"),
            ("label_method", "Method", "Метод"),
            ("label_stoichiometry_anion", "Stoichiometry Anion", "Стехиометрия аниона"),
            ("label_ff", "FF (%)", "FF (%)"),
            ("label_pce", "PCE (%)", "PCE (%)"),
            ("label_voc", "VOC", "VOC"),
            ("label_jsc", "JSC", "JSC"),

            # Растворители и структура
            ("col_type", "Type", "Тип"),
            ("col_symbol", "Symbol", "Символ"),
            ("col_share", "Share", "Доля"),
            ("col_valence", "Valence", "Валентность"),

            # K-факторы
            ("col_salt", "Salt", "Соль"),
            ("col_kfactor", "K-Factor", "K-фактор")
        ]

        self.db.add_batch_translations(default_translations)


# Глобальный экземпляр для удобного доступа
localization_manager = LocalizationManager()