import sqlite3
import tkinter.messagebox as mb

class IonsFormModel:
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

        table_create_query = '''CREATE TABLE IF NOT EXISTS Ions 
                               (name TEXT PRIMARY KEY,
                                type TEXT,
                                valence TEXT, 
                                formula TEXT)'''
        try:
            self.conn.execute(table_create_query)
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to create table: {e}")

    def add_ion(self, name, ion_type, formula, valence):
        if not all([name, formula]):
            return False, "All fields are required"
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? OR formula = ? LIMIT 1",
                           (name, formula))
            if cursor.fetchone():
                return False, "Ion with this name or formula already exists"

            data_insert_query = '''INSERT INTO Ions
                                  (name, type, formula, valence) VALUES 
                                  (?, ?, ?, ?)'''
            cursor.execute(data_insert_query, (name, ion_type, formula, valence))
            self.conn.commit()
            return True, f"{ion_type} successfully uploaded"

        except sqlite3.Error as e:
            return False, f"Database error: {e}"

        finally:
            if self.conn:
                self.conn.close()