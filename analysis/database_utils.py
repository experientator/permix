import sqlite3
import pandas as pd

def get_ionic_radius(name, charge, cn):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ionic_radii FROM Ionic_radii WHERE name = ? AND charge = ? AND cn = ?",
            (name, charge, cn))
        result = cursor.fetchone()
        return float(result[0]) if result else None

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
    return cation_formula[0]

def get_anion_stoichiometry(id_template):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT anion_stoichiometry FROM Phase_templates WHERE id = ?", (id_template,))
    anion_stoichiometry = cursor.fetchone()
    conn.close()
    return int(anion_stoichiometry[0])

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

def get_template_site_types(template_id):
    a_site_config = None
    spacer_config = None
    b_site_config = None
    b_double_config = None

    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT type FROM Template_sites WHERE id_phase = ?",
            (template_id,)
        )
        results_cursor = cursor.fetchall()
        results = [row[0] for row in results_cursor] if results_cursor else []
        if "a_site" in results: a_site_config = True
        if "spacer" in results: spacer_config = True
        if "b_site" in results: b_site_config = True
        if "b_double" in results: b_double_config = True

        return(a_site_config, spacer_config, b_site_config, b_double_config)

def get_template_site_valences(template_id, site_type):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT valence FROM Template_sites WHERE id_phase = ? AND type = ?",
            (template_id, site_type)
        )
        results_cursor = cursor.fetchall()
        return results_cursor[0]

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
