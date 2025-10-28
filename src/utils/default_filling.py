import sqlite3
from src.utils.database_utils import get_template_name
from src.language.manager import localization_manager
from src.utils.calculation_tests import show_error

def get_composition_syntesis(db_path, id_info, notfav):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if notfav:
        query = '''
            SELECT 
                cs.v_antisolvent,
                cs.v_solution, 
                cs.c_solution
            FROM Compositions_info ci
            LEFT JOIN Compositions_syntesis cs ON ci.id = cs.id_info
            WHERE ci.id = ?
            '''
    else:
        query = '''
        SELECT V_antisolvent, V_solution, C_solution
        FROM Fav_compositions 
        WHERE id = ?
        '''
    cursor.execute(query, (id_info,))
    result = cursor.fetchone()
    conn.close()

    return result

def get_template(db_path, id_info, notfav):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if notfav:
        query = '''
        SELECT id_template
        FROM Compositions_info 
        WHERE id = ?
        '''
    else:
        query = '''
                SELECT id_phase
                FROM Fav_compositions 
                WHERE id = ?
                '''
    cursor.execute(query, (id_info,))
    result = cursor.fetchone()
    conn.close()
    name = get_template_name(int(result[0]))
    return name

def get_composition_solvents(db_path, id_info, notfav):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if notfav:
        query = '''
        SELECT solvent_type, symbol, fraction
        FROM Compositions_solvents 
        WHERE id_info = ?
        '''
    else:
        query = '''
               SELECT solvent_type, symbol, fraction
               FROM Compositions_solvents 
               WHERE id_fav = ?
               '''
    cursor.execute(query, (id_info,))
    solvents = cursor.fetchall()
    conn.close()

    return solvents


def get_composition_structures(db_path, id_info, notfav):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if notfav:
        query = '''
        SELECT structure_type, symbol, fraction
        FROM Compositions_structure 
        WHERE id_info = ?
        '''
    else:
        query = '''
               SELECT structure_type, symbol, fraction
               FROM Compositions_structure 
               WHERE id_fav = ?
               '''

    cursor.execute(query, (id_info,))
    structures = cursor.fetchall()
    conn.close()

    return structures

def get_composition_k_factors(db_path, id_info, notfav):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if notfav:
        query = '''
        SELECT  name, k_factor
        FROM K_factors 
        WHERE id_info = ?
        '''
    else:
        query = '''
               SELECT  name, k_factor
               FROM K_factors 
               WHERE id_fav = ?
               '''
    cursor.execute(query, (id_info,))
    k_factors = cursor.fetchall()
    conn.close()

    return k_factors

def get_parameters(id_info, db_path, notfav):
    template_name = get_template(db_path, id_info, notfav)
    v_antisolvent, v_solution, c_solution = get_composition_syntesis(db_path, id_info, notfav)
    syntesis = {
        "v_anti": v_antisolvent,
        "v_sol": v_solution,
        "c_sol": c_solution
    }
    solvents = get_composition_solvents(db_path, id_info, notfav)
    antisol_num = 0
    antisolv = {}
    sol_num = 0
    solv = {}
    sites_num = [0, 0, 0, 0, 0]
    sites = {
        "a_site": {},
        "b_site": {},
        "b_double": {},
        "spacer": {},
        "anion": {}
    }
    for solvent in solvents:
        if solvent[0] == "antisolvent":
            antisol_num += 1
            antisolv[antisol_num-1] = {
                "name": solvent[1],
                "fraction": solvent[2]
            }
        elif solvent[0] == "solvent":
            sol_num += 1
            solv[sol_num - 1] = {
                "name": solvent[1],
                "fraction": solvent[2]
            }
    structure = get_composition_structures(db_path, id_info, notfav)
    for struct in structure:
        if struct[0] == "a_site":
            sites_num[0] += 1
            sites["a_site"][sites_num[0]-1] = {
                "name": struct[1],
                "fraction": struct[2]
            }
        elif struct[0] == "b_site":
            sites_num[1] += 1
            sites["b_site"][sites_num[1] - 1] = {
                "name": struct[1],
                "fraction": struct[2]
            }
        elif struct[0] == "b_double":
            sites_num[2] += 1
            sites["b_double"][sites_num[2] - 1] = {
                "name": struct[1],
                "fraction": struct[2]
            }
        elif struct[0] == "spacer":
            sites_num[3] += 1
            sites["spacer"][sites_num[3] - 1] = {
                "name": struct[1],
                "fraction": struct[2]
            }
        elif struct[0] == "anion":
            sites_num[4] += 1
            sites["anion"][sites_num[4] - 1] = {
                "name": struct[1],
                "fraction": struct[2]
            }
    k_factors = get_composition_k_factors(db_path, id_info, notfav)
    k_f_num = 0
    k_fact = {}
    for k_f in k_factors:
        k_f_num += 1
        k_fact[k_f_num-1] = {
            "salt": k_f[0],
            "k_factor": k_f[1]
        }
    return template_name, syntesis, antisol_num, antisolv, sol_num, solv, sites_num, sites, k_f_num, k_fact

def get_extra_info_parameters(db_path, id_info, notfav):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if notfav:
        query = '''
          SELECT data_type, device_type, doi, name, notes
          FROM Compositions_info 
          WHERE id = ?
          '''
    else:
        query = '''
                  SELECT name, notes
                  FROM Fav_compositions 
                  WHERE id = ?
                  '''
    cursor.execute(query, (id_info,))
    info = cursor.fetchone()
    conn.close()

    return info

def get_extra_synt_parameters(db_path, id_info, notfav):
    if notfav:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = '''
          SELECT stability_notes, method_description
          FROM Compositions_syntesis 
          WHERE id_info = ?
          '''
        cursor.execute(query, (id_info,))
        info = cursor.fetchone()
        conn.close()
        return info
    else:
        return '',''

def get_extra_parameters(db_path, id_info, notfav):
    if notfav:
        data_type, device_type, doi, name, notes = get_extra_info_parameters(db_path, id_info, notfav)
    else:
        name, notes = get_extra_info_parameters(db_path, id_info, notfav)
        data_type = ''
        device_type = ''
        doi = ''
    stab_notes, method_desc = get_extra_synt_parameters(db_path, id_info, notfav)
    extra_param = {
        "data_type": data_type,
        "device_type": device_type,
        "doi": doi,
        "name": name,
        "notes": notes,
        "stab_notes": stab_notes,
        "method_desc": method_desc
    }
    return extra_param

def get_device_properties(composition_id, device_type):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
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