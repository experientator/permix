import sqlite3
from analysis.calculation_tests import show_error
from gui.language.manager import localization_manager

class FavoriteCompositionsModel:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def get_all_favorites(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT fc.id, fc.name, fc.id_phase, pt.name as phase_name, 
                             fc.V_solution, fc.V_antisolvent, fc.C_solution, fc.notes
                             FROM Fav_compositions fc
                             LEFT JOIN Phase_templates pt ON fc.id_phase = pt.id''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            er = localization_manager.tr("fcompf1")
            show_error(f"{er}: {e}")
            return []

    def get_favorite_details(self, favorite_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT fc.*, pt.name as phase_name 
                            FROM Fav_compositions fc
                            LEFT JOIN Phase_templates pt ON fc.id_phase = pt.id
                            WHERE fc.id = ?''', (favorite_id,))
            main_info = cursor.fetchone()

            cursor.execute('''SELECT solvent_type, symbol, fraction 
                            FROM Compositions_solvents 
                            WHERE id_fav = ?''', (favorite_id,))
            solvents = cursor.fetchall()

            cursor.execute('''SELECT structure_type, symbol, fraction, valence 
                            FROM Compositions_structure 
                            WHERE id_fav = ?''', (favorite_id,))
            structure = cursor.fetchall()

            cursor.execute('''SELECT name, k_factor FROM K_factors 
                            WHERE id_fav = ?''', (favorite_id,))
            k_factors = cursor.fetchall()

            return {
                'main_info': main_info,
                'solvents': solvents,
                'structure': structure,
                'k_factors': k_factors
            }
        except sqlite3.Error as e:
            er = localization_manager.tr("fcompf2")
            show_error(f"{er}: {e}")
            return None

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
            er = localization_manager.tr("fcompf3")
            show_error(f"{er}: {e}")
            return None