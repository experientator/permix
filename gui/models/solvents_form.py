import sqlite3
import tkinter.messagebox as mb

class SolventFormModel:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.create_table()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Solvents 
                           (name TEXT PRIMARY KEY,  
                            formula TEXT, 
                            density FLOAT, 
                            boiling_point FLOAT, 
                            notes TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to create table: {e}")

    def add_solvent(self, name, formula, density, boiling_point, notes):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Solvents 
                          (name, formula, density, boiling_point, notes) 
                          VALUES (?, ?, ?, ?, ?)''',
                           (name, formula, density, boiling_point, notes))
            self.conn.commit()
            return True, "Solvent successfully uploaded"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def __del__(self):
        if self.conn:
            self.conn.close()