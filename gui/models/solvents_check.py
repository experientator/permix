import sqlite3
import tkinter.messagebox as mb

class SolventsCheckModel:
    def __init__(self, db_name='data.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def close(self):
        if self.conn:
            self.conn.close()

    def get_all_solvents(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Solvents")
        return cursor.fetchall()

    def delete_solvent(self, name):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Solvents WHERE name=?", (name,))
        self.conn.commit()
        return cursor.rowcount > 0

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Solvents 
                           (name TEXT PRIMARY KEY,
                           type TEXT,  
                            formula TEXT, 
                            density FLOAT, 
                            boiling_point FLOAT, 
                            notes TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to create table: {e}")

    def add_solvent(self, name, type, formula, density, boiling_point, notes):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Solvents 
                          (name, type, formula, density, boiling_point, notes) 
                          VALUES (?, ?, ?, ?, ?, ?)''',
                           (name, type, formula, density, boiling_point, notes))
            self.conn.commit()
            return True, "Solvent successfully uploaded"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"