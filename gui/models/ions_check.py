import sqlite3

class IonsCheckModel:
    def __init__(self, db_name = 'data.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()

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
