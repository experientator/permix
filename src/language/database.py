import sqlite3
import os
import sys

class LocalizationDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Determine OS and set appropriate database path
            if hasattr(sys, 'getwindowsversion'):  # Windows
                # Use AppData directory in Windows
                app_data = os.getenv('APPDATA')
                db_dir = os.path.join(app_data, 'permix') if app_data else os.path.expanduser('~/.permix')
            else:  # Linux/WSL
                # Use /tmp in WSL, home directory in real Linux
                db_dir = os.path.expanduser('~/.permix')

            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'data.db')

            # Copy database from project directory if it doesn't exist
            if not os.path.exists(db_path):
                try:
                    project_db = os.path.join(os.path.dirname(__file__), '../../data.db')
                    if os.path.exists(project_db):
                        import shutil
                        shutil.copy2(project_db, db_path)
                        print(f"Database copied to: {db_path}")
                except Exception as e:
                    print(f"Warning: Could not copy database: {e}")

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
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                'INSERT OR REPLACE INTO localization (name, en, ru) VALUES (?, ?, ?)',
                translations
            )

    def clear_translations(self, language_code: str = None):
        pass