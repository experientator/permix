import sqlite3
from analysis.calculation_tests import show_error
from gui.language.manager import localization_manager

class CompositionCheckModel:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        localization_manager.register_observer(self)

    def get_all_compositions(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT ci.id, ci.name, ci.device_type, ci.doi, ci.data_type, ci.notes, 
                             pt.name as template_name 
                             FROM Compositions_info ci
                             LEFT JOIN Phase_templates pt ON ci.id_template = pt.id''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc1")
            show_error(f"{er}: {e}")
            return []

    def get_composition_details(self, composition_id):
        try:
            cursor = self.conn.cursor()

            # Основная информация о композиции
            cursor.execute('''SELECT ci.*, pt.name as template_name 
                            FROM Compositions_info ci
                            LEFT JOIN Phase_templates pt ON ci.id_template = pt.id
                            WHERE ci.id = ?''', (composition_id,))
            main_info = cursor.fetchone()

            # Растворители
            cursor.execute('''SELECT solvent_type, symbol, fraction 
                            FROM Compositions_solvents 
                            WHERE id_info = ?''', (composition_id,))
            solvents = cursor.fetchall()

            # Структура (ионы)
            cursor.execute('''SELECT structure_type, symbol, fraction, valence 
                            FROM Compositions_structure 
                            WHERE id_info = ?''', (composition_id,))
            structure = cursor.fetchall()

            # Параметры синтеза
            cursor.execute('''SELECT * FROM Compositions_syntesis 
                            WHERE id_info = ?''', (composition_id,))
            synthesis = cursor.fetchone()

            # K-факторы
            cursor.execute('''SELECT name, k_factor FROM K_factors 
                            WHERE id_info = ?''', (composition_id,))
            k_factors = cursor.fetchall()

            # Свойства устройств (в зависимости от типа устройства)
            device_type = main_info[2] if main_info else None  # device_type находится в 3-й колонке (индекс 2)
            properties = self._get_device_properties(composition_id, device_type)

            return {
                'main_info': main_info,
                'solvents': solvents,
                'structure': structure,
                'synthesis': synthesis,
                'properties': properties,
                'k_factors': k_factors
            }
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc2")
            show_error(f"{er}: {e}")
            return None

    def _get_device_properties(self, composition_id, device_type):
        """Получает свойства устройства в зависимости от его типа"""
        try:
            cursor = self.conn.cursor()

            if device_type == localization_manager.tr("ccv_device1"):
                cursor.execute('''SELECT * FROM Solar_cell_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device2"):
                cursor.execute('''SELECT * FROM Photodetectors_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device3"):
                cursor.execute('''SELECT * FROM Direct_x_ray_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device4"):
                cursor.execute('''SELECT * FROM Indirect_x_ray_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device5"):
                cursor.execute('''SELECT * FROM LED_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device6"):
                cursor.execute('''SELECT * FROM Memristors_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device7"):
                cursor.execute('''SELECT * FROM Lasers_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device8"):
                cursor.execute('''SELECT * FROM FET_properties 
                                WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device9"):
                cursor.execute('''SELECT * FROM Thermo_generators_properties 
                                WHERE id_info = ?''', (composition_id,))
            else:
                return None

            return cursor.fetchone()
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc3")
            show_error(f"{er}: {e}")
            return None

    def get_related_data(self, table_name, composition_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'SELECT * FROM {table_name} WHERE id_info = ?', (composition_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc4")
            show_error(f"{er} {table_name}: {e}")
            return []

    def get_all_device_properties(self, composition_id):
        """Получает все свойства устройств для данной композиции"""
        try:
            cursor = self.conn.cursor()
            properties = {}

            # Солнечные элементы
            cursor.execute('SELECT * FROM Solar_cell_properties WHERE id_info = ?', (composition_id,))
            properties['solar_cell'] = cursor.fetchone()

            # Фотодетекторы
            cursor.execute('SELECT * FROM Photodetectors_properties WHERE id_info = ?', (composition_id,))
            properties['photodetector'] = cursor.fetchone()

            # Прямые рентгеновские детекторы
            cursor.execute('SELECT * FROM Direct_x_ray_properties WHERE id_info = ?', (composition_id,))
            properties['direct_xray'] = cursor.fetchone()

            # Косвенные рентгеновские детекторы
            cursor.execute('SELECT * FROM Indirect_x_ray_properties WHERE id_info = ?', (composition_id,))
            properties['indirect_xray'] = cursor.fetchone()

            # LED
            cursor.execute('SELECT * FROM LED_properties WHERE id_info = ?', (composition_id,))
            properties['led'] = cursor.fetchone()

            # Мемристоры
            cursor.execute('SELECT * FROM Memristors_properties WHERE id_info = ?', (composition_id,))
            properties['memristor'] = cursor.fetchone()

            # Лазеры
            cursor.execute('SELECT * FROM Lasers_properties WHERE id_info = ?', (composition_id,))
            properties['laser'] = cursor.fetchone()

            # FET
            cursor.execute('SELECT * FROM FET_properties WHERE id_info = ?', (composition_id,))
            properties['fet'] = cursor.fetchone()

            # Термогенераторы
            cursor.execute('SELECT * FROM Thermo_generators_properties WHERE id_info = ?', (composition_id,))
            properties['thermo_generator'] = cursor.fetchone()

            return properties
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc5")
            show_error(f"{er}: {e}")
            return {}