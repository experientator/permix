import sqlite3
import tkinter.messagebox as mb

class CandidateFormModel:
    def __init__(self):
        self.conn = None
        self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        try:
            self.conn = sqlite3.connect('data.db')
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to connect to database: {e}")

    def create_table(self):
        if not self.conn:
            return

        table_create_query = '''CREATE TABLE IF NOT EXISTS Candidate_cations 
                               (name TEXT PRIMARY KEY,
                                cations TEXT)'''
        try:
            self.conn.execute(table_create_query)
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to create table: {e}")

    def add_candidate(self, name, candidates):
        if not all([name, candidates]):
            return False, "All fields are required"
        try:
            cursor = self.conn.cursor()
            data_insert_query = '''INSERT INTO Candidate_cations
                                  (name, cations) VALUES 
                                  (?, ?)'''
            cursor.execute(data_insert_query, (name, candidates))
            self.conn.commit()
            return True, f"candidate list successfully uploaded"

        except sqlite3.Error as e:
            return False, f"Database error: {e}"

        finally:
            if self.conn:
                self.conn.close()