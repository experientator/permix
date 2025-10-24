import sqlite3

import src.utils.database_utils
from src.utils.calculation_tests import show_error
from src.language.manager import localization_manager

class CompositionCheckModel:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        localization_manager.register_observer(self)

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_info 
                           (id INTEGER PRIMARY KEY,
                           id_template INT,
                           device_type TEXT NULL,
                            name TEXT NULL, 
                            doi TEXT NULL,
                            data_type TEXT NULL, 
                            notes TEXT,
                            FOREIGN KEY (id_template) REFERENCES Phase_templates (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_syntesis 
                                       (id_info INT,
                                        stability_notes TEXT NULL,
                                        v_antisolvent FLOAT NULL,
                                        v_solution FLOAT NULL,
                                        c_solution FLOAT NULL,
                                        method_description TEXT NULL,
                                        FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')


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

            cursor.execute('''CREATE TABLE IF NOT EXISTS Solar_cell_properties 
                           (id_info INT NULL,
                            pce FLOAT NULL,
                            v_oc FLOAT NULL, 
                            j_sc FLOAT NULL, 
                            ff FLOAT NULL,
                            eqe FLOAT NULL,
                            op_stab FLOAT NULL,  
                            hyst_ind FLOAT NULL,
                            FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Photodetectors_properties 
                                       (id_info INT NULL,
                                        resp FLOAT NULL,
                                        sd FLOAT NULL, 
                                        eqe FLOAT NULL, 
                                        rf_time FLOAT NULL,
                                        ldr FLOAT NULL,
                                        nep FLOAT NULL,  
                                        srr FLOAT NULL,
                                        FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Direct_x_ray_properties 
                                                   (id_info INT NULL,
                                                    cce FLOAT NULL,
                                                    sens FLOAT NULL, 
                                                    lod FLOAT NULL, 
                                                    mlp FLOAT NULL,
                                                    sp_res FLOAT NULL,
                                                    dc FLOAT NULL,  
                                                    sts FLOAT NULL,
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Indirect_x_ray_properties 
                                                   (id_info INT NULL,
                                                    light_y FLOAT NULL,
                                                    lod FLOAT NULL, 
                                                    sp_res FLOAT NULL, 
                                                    aft_gl FLOAT NULL,
                                                    sdt FLOAT NULL,
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS LED_properties 
                                                   (id_info INT NULL,
                                                    eqe FLOAT NULL,
                                                    lum FLOAT NULL,
                                                    cie FLOAT NULL, 
                                                    fwhm FLOAT NULL, 
                                                    turn_volt FLOAT NULL,
                                                    lt FLOAT NULL,
                                                    ce FLOAT NULL,  
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Memristors_properties 
                                                   (id_info INT NULL,
                                                    res_rat FLOAT NULL,
                                                    end FLOAT NULL, 
                                                    r_time FLOAT NULL, 
                                                    ss FLOAT NULL,
                                                    sr_volt FLOAT NULL,
                                                    mc FLOAT NULL,  
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Lasers_properties 
                                                   (id_info INT NULL,
                                                    lt FLOAT NULL,
                                                    q_fact FLOAT NULL, 
                                                    lole FLOAT NULL, 
                                                    dqe FLOAT NULL,
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS FET_properties 
                                                   (id_info INT NULL,
                                                    cm FLOAT NULL,
                                                    c_rat FLOAT NULL, 
                                                    t_volt FLOAT NULL, 
                                                    ss FLOAT NULL,
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS Thermo_generators_properties 
                                                   (id_info INT NULL,
                                                    zt FLOAT NULL,
                                                    s FLOAT NULL, 
                                                    sigma FLOAT NULL, 
                                                    thermal_cond FLOAT NULL,
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id))''')

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

    def delete_selected(self, info_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Compositions_structure WHERE id_info = ?", (info_id,))
            cursor.execute("DELETE FROM Compositions_solvents WHERE id_info = ?", (info_id,))
            cursor.execute("DELETE FROM K_factors WHERE id_info = ?", (info_id,))
            cursor.execute("DELETE FROM Compositions_syntesis WHERE id_info = ?", (info_id,))
            self.conn.commit()
            cursor.execute('''SELECT ci.*
                                        FROM Compositions_info ci
                                        LEFT JOIN Phase_templates pt ON ci.id_template = pt.id
                                        WHERE ci.id = ?''', (info_id,))
            main_info = cursor.fetchone()
            device_type = main_info[2] if main_info else None
            self._delete_device_properties(info_id, device_type)
            cursor.execute("DELETE FROM Compositions_info WHERE id = ?", (info_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            er = localization_manager.tr("fcompf2")
            show_error(f"{er}: {e}")
            return None

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

            cursor.execute('''SELECT ci.*
                            FROM Compositions_info ci
                            LEFT JOIN Phase_templates pt ON ci.id_template = pt.id
                            WHERE ci.id = ?''', (composition_id,))
            main_info = cursor.fetchone()
            main_info = list(main_info)
            main_info[1] = src.utils.database_utils.get_template_name(main_info[1])

            cursor.execute('''SELECT solvent_type, symbol, fraction 
                            FROM Compositions_solvents 
                            WHERE id_info = ?''', (composition_id,))
            solvents = cursor.fetchall()

            cursor.execute('''SELECT structure_type, symbol, fraction, valence 
                            FROM Compositions_structure 
                            WHERE id_info = ?''', (composition_id,))
            structure = cursor.fetchall()

            cursor.execute('''SELECT * FROM Compositions_syntesis 
                            WHERE id_info = ?''', (composition_id,))
            synthesis = cursor.fetchone()

            cursor.execute('''SELECT name, k_factor FROM K_factors 
                            WHERE id_info = ?''', (composition_id,))
            k_factors = cursor.fetchall()

            device_type = main_info[2] if main_info else None
            properties = self._get_device_properties(composition_id, device_type)

            return {
                'main_info': main_info,
                'solvents': solvents,
                'structure': structure,
                'synthesis': synthesis,
                'properties': properties,
                'k_factors': k_factors,
                'device_type': device_type
            }
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc2")
            show_error(f"{er}: {e}")
            return None

    def _get_device_properties(self, composition_id, device_type):
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
            prop = list(cursor.fetchone())
            prop.pop(0)
            return prop
        except sqlite3.Error as e:
            er = localization_manager.tr("mcompc3")
            show_error(f"{er}: {e}")
            return None

    def _delete_device_properties(self, composition_id, device_type):
        try:
            cursor = self.conn.cursor()

            if device_type == localization_manager.tr("ccv_device1"):
                cursor.execute('''DELETE FROM Solar_cell_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device2"):
                cursor.execute('''DELETE FROM Photodetectors_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device3"):
                cursor.execute('''DELETE FROM Direct_x_ray_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device4"):
                cursor.execute('''DELETE FROM Indirect_x_ray_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device5"):
                cursor.execute('''DELETE FROM LED_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device6"):
                cursor.execute('''DELETE FROM Memristors_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device7"):
                cursor.execute('''DELETE FROM Lasers_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device8"):
                cursor.execute('''DELETE FROM FET_properties 
                                   WHERE id_info = ?''', (composition_id,))
            elif device_type == localization_manager.tr("ccv_device9"):
                cursor.execute('''DELETE FROM Thermo_generators_properties 
                                   WHERE id_info = ?''', (composition_id,))
            else:
                return None
            self.conn.commit()
            return None
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