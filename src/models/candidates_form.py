import sqlite3
from src.utils.calculation_tests import show_error
from src.language.manager import localization_manager

class CandidateFormModel:
    def __init__(self):
        self.conn = None
        self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        try:
            self.conn = sqlite3.connect('data.db')
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err1")
            show_error( f"{er}: {e}")

    def create_table(self):
        if not self.conn:
            return

        table_create_query = '''CREATE TABLE IF NOT EXISTS Candidate_cations 
                               (name TEXT PRIMARY KEY,
                                cations TEXT)'''
        try:
            self.conn.execute(table_create_query)
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err2")
            show_error(f"{er}: {e}")

    def add_candidate(self, name, candidates):
        if not all([name, candidates]):
            return False, localization_manager.tr("mcanf2")
        try:
            cursor = self.conn.cursor()
            data_insert_query = '''INSERT INTO Candidate_cations
                                  (name, cations) VALUES 
                                  (?, ?)'''
            cursor.execute(data_insert_query, (name, candidates))
            self.conn.commit()
            return True, localization_manager.tr("mcanf1")

        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

        finally:
            if self.conn:
                self.conn.close()