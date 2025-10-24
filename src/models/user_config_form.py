import sqlite3
from src.utils.calculation_tests import show_error
from src.language.manager import localization_manager
from collections import namedtuple

Numbers = namedtuple("Numbers", ["elements", "solvent"])

class UserConfigModel:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.create_tables()

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Fav_compositions
                           (id INTEGER PRIMARY KEY,
                            name TEXT NULL, 
                            id_phase INT,
                            V_solution FLOAT,
                            V_antisolvent FLOAT NULL,
                            C_solution FLOAT,  
                            notes TEXT NULL,
                            FOREIGN KEY (id_phase) REFERENCES Phase_templates (id))''')

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

            cursor.execute('''CREATE TABLE IF NOT EXISTS K_factors 
                                                (id_info INT NULL,
                                                id_fav INT NULL,
                                                name TEXT,
                                                k_factor FLOAT,
                                                FOREIGN KEY (id_info) REFERENCES Compositions_info (id)
                                                FOREIGN KEY (id_fav) REFERENCES Fav_compositions (id))''')

            self.conn.commit()
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err2")
            show_error(f"{er}: {e}")

    def add_favorite_composition(self, name, id_phase, notes, v_sol, v_antisol, c_sol, upd=False, id_fav=None):
        try:
            cursor = self.conn.cursor()
            if upd:
                cursor.execute('''UPDATE Fav_compositions  
                              SET name = ?, id_phase = ?, V_solution = ?, V_antisolvent = ?, C_solution = ?, notes = ?
                              WHERE id = ?''',
                               (name, id_phase, v_sol, v_antisol, c_sol, notes, id_fav))
                self.conn.commit()
                cursor.close()
                return id_fav  # Возвращаем тот же id_fav
            else:
                cursor.execute('''INSERT INTO Fav_compositions  
                              (name, id_phase, V_solution, V_antisolvent, C_solution, notes) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                               (name, id_phase, v_sol, v_antisol, c_sol, notes))
                self.conn.commit()
                new_id = cursor.lastrowid
                cursor.close()
                return new_id
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompf2")
            show_error(f"{er}: {e}")
            return None

    def add_solvent(self, id_fav, solvent_type, symbol, fraction, upd=False):
        try:
            cursor = self.conn.cursor()

            if upd:
                cursor.execute('''DELETE FROM Compositions_solvents 
                               WHERE id_fav = ?''', (id_fav,))

            cursor.execute("SELECT 1 FROM Solvents WHERE name = ?", (symbol,))
            if not cursor.fetchone():
                er = localization_manager.tr("mcompf3")
                return False, f"{er}: {symbol}"

            cursor.execute('''INSERT INTO Compositions_solvents 
                          (id_fav, solvent_type, symbol, fraction) 
                          VALUES (?, ?, ?, ?)''',
                           (id_fav, solvent_type, symbol, fraction))
            self.conn.commit()

            message = localization_manager.tr("mcompf4_update") if upd else localization_manager.tr("mcompf4")
            return True, message
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

    def add_structure(self, id_fav, structure_type, symbol, fraction, valence, upd=False):
        try:
            cursor = self.conn.cursor()

            if upd:
                cursor.execute('''DELETE FROM Compositions_structure 
                               WHERE id_fav = ?''', (id_fav,))

            ion_type = "anion" if structure_type == "anion" else "cation"
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? AND type = ?",
                           (symbol, ion_type))
            if not cursor.fetchone():
                er = localization_manager.tr("mcompf6")
                return False, f"{er}: {symbol}"

            cursor.execute('''INSERT INTO Compositions_structure 
                          (id_fav, structure_type, symbol, fraction, valence) 
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_fav, structure_type, symbol, fraction, valence))
            self.conn.commit()

            message = localization_manager.tr("mcompf7_update") if upd else localization_manager.tr("mcompf7")
            return True, message
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

    def add_k_factors(self, id_fav, salt, k_factor, upd=False):
        try:
            cursor = self.conn.cursor()

            if upd:
                cursor.execute('''DELETE FROM K_factors 
                               WHERE id_fav = ?''', (id_fav,))

            cursor.execute('''INSERT INTO K_factors 
                          (id_fav, name, k_factor) 
                          VALUES (?, ?, ?)''',
                           (id_fav, salt, k_factor))
            self.conn.commit()

            message = localization_manager.tr("mcompf5_update") if upd else localization_manager.tr("mcompf5")
            return True, message
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

    def __del__(self):
        if self.conn:
            self.conn.close()