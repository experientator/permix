import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional

import sqlite3
import os
from typing import List, Dict, Any, Optional

def get_database_path() -> str:
    """Get the path to the database file"""
    return 'data.db'

def get_template_id(template_name: str) -> Optional[int]:
    db_path = get_database_path()
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Phase_templates WHERE name = ?", (template_name,))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error:
        return None

def get_connection():
    """Get database connection"""
    return sqlite3.connect(get_database_path())

# Add other database utility functions as needed
def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    db_path = get_database_path()
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def execute_update(query: str, params: tuple = ()) -> int:
    """Execute an update query and return number of affected rows"""
    db_path = get_database_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount

def get_templates_list() -> List[Dict[str, Any]]:
    db_path = get_database_path()
    import sqlite3
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM Phase_templates")
        return [dict(row) for row in cursor.fetchall()]

def get_cation_list_by_key(key):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT cations FROM Candidate_cations WHERE name = ?", (key,))
    cations = cursor.fetchone()
    conn.close()
    return cations[0]

def get_ionic_radius(name, charge, cn):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ionic_radii FROM Ionic_radii WHERE name = ? AND charge = ? AND cn = ?",
            (name, charge, cn))
        result = cursor.fetchone()
        return float(result[0]) if result else None

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

def get_dimensionality(id_template):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT dimensionality FROM Phase_templates WHERE id = ?", (id_template,))
    dimensionality = cursor.fetchone()
    conn.close()
    return int(dimensionality[0])

def get_fav_id(name):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM Fav_compositions WHERE name = ?", (name,))
    id_fav = cursor.fetchone()
    conn.close()
    return int(id_fav[0])

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

        return a_site_config, spacer_config, b_site_config, b_double_config

def get_template_site_valences(template_id, site_type):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT valence FROM Template_sites WHERE id_phase = ? AND type = ?",
        (template_id, site_type)
    )
    results_cursor = cursor.fetchone()
    conn.close()
    return float(results_cursor[0])

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

def get_template_name(id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM Phase_templates WHERE id = ?", (id,))
    name = cursor.fetchone()
    conn.close()
    return name[0]

def get_template_ions(template_id: int) -> List[Dict[str, Any]]:
    db_path = get_database_path()
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM template_ions WHERE template_id = ?", (template_id,))
        return [dict(row) for row in cursor.fetchall()]