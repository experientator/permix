import sqlite3
import pandas as pd

def get_templates_list():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT name FROM Phase_templates ORDER BY dimensionality")
    values = [row[0] for row in cursor.fetchall()]
    conn.close()
    return values

def get_cation_formula(cation_name):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT formula FROM Ions WHERE name = ?", (cation_name,))
    cation_formula = cursor.fetchone()
    conn.close()
    return int(cation_formula[0])

def get_template_id(name):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM Phase_templates WHERE name = ?", (name,))
    id_phase = cursor.fetchone()
    conn.close()
    return int(id_phase[0])

def get_template_sites(template_id):
    conn = sqlite3.connect("data.db")
    sites_data = pd.read_sql_query(f"SELECT type, name_candidate, stoichiometry, valence "
                   f"FROM Template_sites WHERE id_phase = {template_id}", conn)
    conn.close()
    return sites_data

def get_candidate_cations(name):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT cations FROM Candidate_cations WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    cations_text = result[0]
    cations_list = [x.strip() for x in cations_text.split(",")]
    return cations_list

def get_solvents(solvent_type):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT name FROM Solvents WHERE type = ?", (solvent_type,))
    values = [row[0] for row in cursor.fetchall()]
    conn.close()
    return values
