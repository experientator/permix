import sqlite3
from analysis.calculation_tests import show_error
from gui.language.manager import localization_manager

class TemplatesCheckModel:
    def __init__(self, db_name = 'data.db'):
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()

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

    def delete_template(self, id_phase):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Template_sites WHERE id_phase=?", (id_phase,))
        cursor.execute("DELETE FROM Phase_templates WHERE id=?", (id_phase,))
        self.conn.commit()
        return cursor.rowcount > 0

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Phase_templates
                          (id INTEGER PRIMARY KEY,
                           name TEXT,
                           description TEXT NULL,
                           anion_stoichiometry INT,
                           dimensionality INT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Template_sites
                          (id_phase TEXT,
                           stoichiometry INT,
                           type TEXT,
                           valence TEXT,
                           name_candidate TEXT NULL,
                           FOREIGN KEY (id_phase) REFERENCES Phase_templates (id),
                           FOREIGN KEY (name_candidate) REFERENCES Candidate_cations (name))''')

            self.conn.commit()
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err2")
            show_error(f"{er}: {e}")

    def add_template(self, name, description, anion_stoich, dimensionality):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Phase_templates WHERE name = ? LIMIT 1", (name,))
            if cursor.fetchone():
                return None, localization_manager.tr("mtempc1")

            cursor.execute('''INSERT INTO Phase_templates
                          (name, description, anion_stoichiometry, dimensionality)
                          VALUES (?, ?, ?, ?)''',
                           (name, description, anion_stoich, dimensionality))
            self.conn.commit()

            return cursor.lastrowid, localization_manager.tr("mtempc2")
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return None, f"{er}: {e}"

    def add_site(self, template_id, stoichiometry, site_type, valence):
        try:
            cursor = self.conn.cursor()
            name_candidate = f"{site_type}_val_{valence}"

            cursor.execute('''INSERT INTO Template_sites
                          (id_phase, stoichiometry, type, valence, name_candidate)
                          VALUES (?, ?, ?, ?, ?)''',
                           (template_id, stoichiometry, site_type, valence, name_candidate))
            self.conn.commit()

            return True, localization_manager.tr("mtempc3")
        except sqlite3.Error as e:
            er = localization_manager.tr("db_err3")
            return False, f"{er}: {e}"

    def get_last_template_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM Phase_templates ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            er = localization_manager.tr("mtempc4")
            show_error(f"{er}: {e}")
            return None

    def __del__(self):
        if self.conn:
            self.conn.close()
