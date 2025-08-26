import sqlite3
from tkinter import messagebox as mb

class CompositionCheckModel:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def get_all_compositions(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT ci.id, ci.name, ci.doi, ci.data_type, ci.notes, 
                             pt.name as template_name 
                             FROM Compositions_info ci
                             LEFT JOIN Phase_templates pt ON ci.id_template = pt.id''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to get compositions: {e}")
            return []

    def get_composition_details(self, composition_id):
        try:
            cursor = self.conn.cursor()

            cursor.execute('''SELECT ci.*, pt.name as template_name 
                            FROM Compositions_info ci
                            LEFT JOIN Phase_templates pt ON ci.id_template = pt.id
                            WHERE ci.id = ?''', (composition_id,))
            main_info = cursor.fetchone()

            cursor.execute('''SELECT solvent_type, symbol, fraction 
                            FROM Compositions_solvents 
                            WHERE id_info = ?''', (composition_id,))
            solvents = cursor.fetchall()

            cursor.execute('''SELECT structure_type, symbol, fraction, valence 
                            FROM Compositions_structure 
                            WHERE id_info = ?''', (composition_id,))
            structure = cursor.fetchall()

            cursor.execute('''SELECT * FROM Compositions_properties 
                            WHERE id_info = ?''', (composition_id,))
            properties = cursor.fetchone()

            cursor.execute('''SELECT name, k_factor FROM K_factors 
                            WHERE id_info = ?''', (composition_id,))
            k_factors = cursor.fetchall()

            return {
                'main_info': main_info,
                'solvents': solvents,
                'structure': structure,
                'properties': properties,
                'k_factors': k_factors
            }
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to get composition details: {e}")
            return None

    def get_related_data(self, table_name, composition_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name} WHERE id_info = ?', (composition_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to get {table_name} data: {e}")
            return []