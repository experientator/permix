import sqlite3

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