import sqlite3

class LocalizationDB:
    def __init__(self, db_path="data.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS localization (
                    name TEXT PRIMARY KEY,
                    en TEXT NOT NULL,
                    ru TEXT NOT NULL
                )
            ''')

    def get_translation(self, language, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT {} FROM localization WHERE name = ?'.format(language),
                (name,)
            )
            result = cursor.fetchone()
            return result[0] if result else name

    def get_all_translations(self, language):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f'SELECT name, {language} FROM localization')
            return {row[0]: row[1] for row in cursor.fetchall()}

    def add_translation(self, name, en, ru):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT OR REPLACE INTO localization (name, en, ru) VALUES (?, ?, ?)',
                (name, en, ru)
            )

    def add_batch_translations(self, translations: list):
        """Добавить несколько переводов сразу"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                'INSERT OR REPLACE INTO localization (name, en, ru) VALUES (?, ?, ?)',
                translations
            )