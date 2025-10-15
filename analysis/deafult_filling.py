import sqlite3
from analysis.database_utils import get_template_name

def get_composition_syntesis(db_path, id_info):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT 
        cs.v_antisolvent,
        cs.v_solution, 
        cs.c_solution,
    FROM Compositions_info ci
    LEFT JOIN Compositions_syntesis cs ON ci.id = cs.id_info
    WHERE ci.id = ?
    '''

    cursor.execute(query, (id_info,))
    result = cursor.fetchone()
    conn.close()

    return result

def get_template(db_path, id_info):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT id_template
    FROM Compositions_info 
    WHERE id = ?
    '''
    cursor.execute(query, (id_info,))
    result = cursor.fetchone()
    conn.close()
    name = get_template_name(int(result[0]))
    return name

def get_composition_solvents(db_path, id_info):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT solvent_type, symbol, fraction
    FROM Compositions_solvents 
    WHERE id_info = ?
    '''

    cursor.execute(query, (id_info,))
    solvents = cursor.fetchall()
    conn.close()

    return solvents


def get_composition_structures(db_path, id_info):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT structure_type, symbol, fraction
    FROM Compositions_structure 
    WHERE id_info = ?
    '''

    cursor.execute(query, (id_info,))
    structures = cursor.fetchall()
    conn.close()

    return structures

def get_composition_k_factors(db_path, id_info):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT  name, k_factor
    FROM K_factors 
    WHERE id_info = ?
    '''

    cursor.execute(query, (id_info,))
    k_factors = cursor.fetchall()
    conn.close()

    return k_factors

def get_parameters(fav, id_info, db_path):
    v_antisolvent, v_solution, c_solution = get_composition_syntesis(db_path, id_info)
    solvents = get_composition_solvents(db_path, id_info)
    antisol_num = 0
    antisolv = []
    sol_num = 0
    solv = []
    for solvent in solvents:
        if solvent[0] == "antisolvent":
            antisol_num += 1
            antisolv.append(solvent)
        elif solvent[0] == "solvent":
            sol_num += 1
            solv.append(solvent)
    structure = get_composition_structures(db_path, id_info)
    k_factors = get_composition_k_factors(db_path, id_info)