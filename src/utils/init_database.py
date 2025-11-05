import sqlite3
import os

def init_database():
    db_path = "data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу templates если её нет
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Candidate_cations 
                               (name TEXT PRIMARY KEY,
                                cations TEXT)
    ''')

    # Создаем другие необходимые таблицы
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

    cursor.execute('''CREATE TABLE IF NOT EXISTS Ionic_radii 
                                (name TEXT,
                                 ion_type TEXT,
                                 charge INT, 
                                 CN INT,
                                 ionic_radii FLOAT,
                                 FOREIGN KEY (name) REFERENCES Ions (name))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Ions 
                                               (name TEXT PRIMARY KEY,
                                                type TEXT,
                                                valence TEXT, 
                                                formula TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Solvents 
                               (name TEXT PRIMARY KEY,
                               type TEXT,  
                                formula TEXT, 
                                density FLOAT, 
                                boiling_point FLOAT, 
                                notes TEXT)''')
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS Fav_compositions
                               (id INTEGER PRIMARY KEY,
                                name TEXT NULL, 
                                id_phase INT,
                                V_solution FLOAT,
                                V_antisolvent FLOAT NULL,
                                C_solution FLOAT,  
                                notes TEXT NULL,
                                FOREIGN KEY (id_phase) REFERENCES Phase_templates (id))''')

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

    cursor.execute('''CREATE TABLE IF NOT EXISTS K_factors 
                                                    (id_info INT NULL,
                                                    id_fav INT NULL,
                                                    name TEXT,
                                                    k_factor FLOAT,
                                                    FOREIGN KEY (id_info) REFERENCES Compositions_info (id)
                                                    FOREIGN KEY (id_fav) REFERENCES Fav_compositions (id))''')

    conn.commit()
    conn.close()
    print("Database initialized successfully")


if __name__ == "__main__":
    init_database()