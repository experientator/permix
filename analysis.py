import sqlite3

def get_templates_list():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT DISTINCT name FROM Phase_templates ORDER BY dimensionality")
    values = [row[0] for row in cursor.fetchall()]

    conn.close()
    return values