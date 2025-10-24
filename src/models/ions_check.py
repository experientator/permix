import sqlite3
from src.utils.calculation_tests import show_error
from src.language.manager import localization_manager

class IonsCheckModel:
    def __init__(self, db_name = 'data.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()
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
            cursor.execute('''CREATE TABLE IF NOT EXISTS Ions 
                                           (name TEXT PRIMARY KEY,
                                            type TEXT,
                                            valence TEXT, 
                                            formula TEXT)''')
            self.conn.commit()
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err2")
            show_error(f"{er}: {e}")

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
            return True, localization_manager.tr("mionc1")
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

    def add_ion(self, name, ion_type, formula, valence):
        if not all([name, formula]):
            return False, localization_manager.tr("mionc2")
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? OR formula = ? LIMIT 1",
                           (name, formula))
            if cursor.fetchone():
                return False, localization_manager.tr("mionc3")

            data_insert_query = '''INSERT INTO Ions
                                  (name, type, formula, valence) VALUES 
                                  (?, ?, ?, ?)'''
            cursor.execute(data_insert_query, (name, ion_type, formula, valence))
            self.conn.commit()
            er = localization_manager.tr("mionc4")
            return True, f"{ion_type} {er}"

        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def get_all_ions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, type FROM Ions ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]

    def get_ionic_radii_for_ion(self, ion_name, ion_type):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT charge, CN, ionic_radii 
        FROM Ionic_radii 
        WHERE name = ? AND ion_type = ?
        ORDER BY charge, CN
        """, (ion_name, ion_type))
        return [dict(row) for row in cursor.fetchall()]

    def delete_ionic_radii(self, name, charge, CN, ionic_radii):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Ionic_radii WHERE name=? AND charge=? AND CN=? AND ionic_radii=?"
                       , (name,charge, CN, ionic_radii))
        self.conn.commit()
        return cursor.rowcount > 0

    def __del__(self):
        if self.conn:
            self.conn.close()