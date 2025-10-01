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
            self.current_language = 'en'
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
        translation = self.translations.get(name)
        if translation:
            return translation
        else:
            print(f"Translation not found for key: '{name}'")  # Debug
            return name  # Возвращаем ключ, если перевод не найден

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

    def initialize_default_translations(self, default_translations):
        self.db.add_batch_translations(default_translations)


# Глобальный экземпляр для удобного доступа
localization_manager = LocalizationManager()