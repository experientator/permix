import sqlite3
import tkinter.messagebox as mb

class IonicRadiiModel:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.create_tables()

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Ionic_radii 
                            (name TEXT,
                             ion_type TEXT,
                             charge INT, 
                             CN INT,
                             ionic_radii FLOAT,
                             FOREIGN KEY (name) REFERENCES Ions (name))''')
            self.conn.commit()
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to create tables: {e}")

    def validate_ion_exists(self, name, ion_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM Ions WHERE name = ? AND type = ?", (name, ion_type))
        return cursor.fetchone() is not None

    def validate_radii_exists(self, name, charge, CN):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM Ionic_radii WHERE name = ? AND charge = ? AND CN = ?",
                       (name, charge, CN))
        return cursor.fetchone() is not None

    def add_ionic_radii(self, name, ion_type, charge, CN, ionic_radii):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Ionic_radii
                              (name, ion_type, charge, CN, ionic_radii) 
                              VALUES (?, ?, ?, ?, ?)''',
                           (name, ion_type, charge, CN, ionic_radii))
            self.conn.commit()
            return True, "Ion radii successfully uploaded"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()