import sqlite3

class TemplatesCheckModel:
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

    def get_all_templates(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, anion_stoichiometry, dimensionality, description FROM Phase_templates ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]

    def get_sites_for_template(self, id_phase):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT type, stoichiometry, valence 
        FROM Template_sites 
        WHERE id_phase = ?
        ORDER BY type
        """, (id_phase,))
        return [dict(row) for row in cursor.fetchall()]
