import sqlite3
import tkinter.messagebox as mb
from collections import namedtuple

Numbers = namedtuple("Numbers", ["elements", "solvent"])


class CompositionModel:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.create_tables()

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_info 
                           (id INTEGER PRIMARY KEY,
                            name TEXT NULL, 
                            doi TEXT NULL,
                            data_type TEXT NULL, 
                            notes TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_solvents
                           (id_info INT NULL,
                            id_fav INT NULL,
                            solvent_type TEXT, 
                            symbol TEXT, 
                            fraction FLOAT,
                            FOREIGN KEY (id_info) REFERENCES Compositions_info (id),
                            FOREIGN KEY (id_fav) REFERENCES Fav_compositions (id),
                            FOREIGN KEY (symbol) REFERENCES Solvents (name))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_structure 
                           (id_info INT NULL,
                            id_fav INT NULL,
                            structure_type TEXT, 
                            symbol TEXT, 
                            fraction FLOAT,
                            valence FLOAT,
                            FOREIGN KEY (id_info) REFERENCES Compositions_info (id),
                            FOREIGN KEY (id_fav) REFERENCES Fav_compositions (id),
                            FOREIGN KEY (symbol) REFERENCES Ions (name))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_properties 
                           (id_info INT NULL,
                            band_gap FLOAT NULL, 
                            ff_percent FLOAT NULL, 
                            pce_percent FLOAT NULL,
                            voc FLOAT NULL,
                            jsc FLOAT NULL,  
                            stability_notes TEXT NULL,
                            v_antisolvent FLOAT NULL,
                            anion_stoichiometry FLOAT NULL,
                            FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            self.conn.commit()
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to create tables: {e}")

    def add_composition_info(self, doi, data_type, notes):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Compositions_info  
                          (doi, data_type, notes) VALUES (?, ?, ?)''',
                           (doi, data_type, notes))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to add composition info: {e}")
            return None

    def add_solvent(self, id_info, solvent_type, symbol, fraction):
        try:
            # Проверка существования растворителя
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Solvents WHERE name = ?", (symbol,))
            if not cursor.fetchone():
                return False, f"Solvent {symbol} doesn't exist in database"

            cursor.execute('''INSERT INTO Compositions_solvents 
                          (id_info, solvent_type, symbol, fraction) 
                          VALUES (?, ?, ?, ?)''',
                           (id_info, solvent_type, symbol, fraction))
            self.conn.commit()
            return True, "Solvent added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_structure(self, id_info, structure_type, symbol, fraction, valence):
        try:
            # Определение типа иона и проверка его существования
            ion_type = "anion" if structure_type == "anion" else "cation"
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? AND ion_type = ?",
                           (symbol, ion_type))
            if not cursor.fetchone():
                return False, f"Ion {symbol} doesn't exist in database"

            cursor.execute('''INSERT INTO Compositions_structure 
                          (id_info, structure_type, symbol, fraction, valence) 
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_info, structure_type, symbol, fraction, valence))
            self.conn.commit()
            return True, "Structure element added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Compositions_properties 
                          (id_info, band_gap, ff_percent, pce_percent, voc, jsc, 
                           stability_notes, v_antisolvent, anion_stoichiometry)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def __del__(self):
        if self.conn:
            self.conn.close()