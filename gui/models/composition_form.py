import sqlite3
import tkinter.messagebox as mb
from collections import namedtuple

from pyexpat.errors import messages

from gui.language.manager import localization_manager

Numbers = namedtuple("Numbers", ["elements", "solvent"])


class CompositionModel:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        localization_manager.register_observer(self)
        self.create_tables()

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Compositions_info 
                           (id INTEGER PRIMARY KEY,
                           id_template INT,
                           device_type TEXT NULL,
                           anion_stoichiometry FLOAT NULL,
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
            mb.showerror("Database Error", f"Failed to create tables: {e}")

    def add_syntesis_params(self, id_info, syntesis_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Compositions_syntesis 
                            (id_info, stability_notes, v_antisolvent, v_solution, c_solution, method_description)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                           (id_info, *syntesis_data))
            self.conn.commit()
            return True, "Syntesis parameters added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_composition_info(self, id_template, comp_info):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Compositions_info  
                          (id_template, device_type, doi, data_type, notes) 
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_template, *comp_info,))
            self.conn.commit()

            new_id = cursor.lastrowid
            cursor.close()

            return new_id
        except sqlite3.Error as e:
            mb.showerror("Database Error", f"Failed to add composition info: {e}")
            return None

    def add_solvent(self, id_info, solvent_type, symbol, fraction):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Solvents WHERE name = ? AND type = ?", (symbol, solvent_type))
            if not cursor.fetchone():
                return False, f"Solvent {symbol} doesn't exist in database"

            cursor.execute('''INSERT INTO Compositions_solvents 
                          (id_info, solvent_type, symbol, fraction) 
                          VALUES (?, ?, ?, ?)''',
                           (id_info, solvent_type, symbol, fraction))
            self.conn.commit()
            return True, "Solvent added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_k_factors(self, id_info, name, k_factor):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO K_factors 
                          (id_info, name, k_factor) 
                          VALUES (?, ?, ?)''',
                           (id_info, name, k_factor))
            self.conn.commit()
            return True, "K-factors added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_structure(self, id_info, structure_type, symbol, fraction, valence):
        try:
            ion_type = "anion" if structure_type == "anion" else "cation"
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM Ions WHERE name = ? AND type = ?",
                           (symbol, ion_type))
            if not cursor.fetchone():
                return False, f"Ion {symbol} doesn't exist in database"

            cursor.execute('''INSERT INTO Compositions_structure 
                          (id_info, structure_type, symbol, fraction, valence) 
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_info, structure_type, symbol, fraction, valence))
            self.conn.commit()
            return True, "Structure element added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_solar_cell_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Solar_cell_properties 
                          (id_info, pce, v_oc, j_sc, ff, eqe, 
                           op_stab, hyst_ind)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_photodetector_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Photodetectors_properties 
                          (id_info, resp, sd, eqe,rf_time, ldr, nep, srr)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_direct_xray_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Direct_x_ray_properties 
                          (id_info, cce, sens, lod, mlp, sp_res, dc, sts)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_indirect_xray_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Indirect_x_ray_properties 
                          (id_info, light_y, lod, sp_res, aft_gl, sdt)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_led_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO LED_properties 
                          (id_info, lum, cie, fwhm, turn_volt, lt, ce)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_memristors_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Memristors_properties 
                          (id_info, res_rat, end, r_time, ss, sr_volt, mc)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_lasers_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Lasers_properties 
                          (id_info, lt, q_fact, lole, dqe)
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_fet_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO FET_properties 
                          (id_info, cm, c_rat, t_volt, ss)
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_thermo_generators_properties(self, id_info, properties_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO Thermo_generators_properties 
                          (id_info, zt, s, sigma, thermal_cond)
                          VALUES (?, ?, ?, ?, ?)''',
                           (id_info, *properties_data))
            self.conn.commit()
            return True, "Properties added successfully"
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def add_properties(self, id_info, device_type, properties_data):
        if device_type == localization_manager.tr("ccv_device1"):
            success, message = self.add_solar_cell_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device2"):
            success, message = self.add_photodetector_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device3"):
            success, message = self.add_direct_xray_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device4"):
            success, message = self.add_indirect_xray_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device5"):
            success, message = self.add_led_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device6"):
            success, message = self.add_memristors_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device7"):
            success, message = self.add_lasers_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device8"):
            success, message = self.add_fet_properties(id_info, properties_data)
        elif device_type == localization_manager.tr("ccv_device9"):
            success, message = self.add_thermo_generators_properties(id_info, properties_data)
        else:
            return "error", "no device..."
        return success, message

    def __del__(self):
        if self.conn:
            self.conn.close()