import re
import periodictable
from analysis.database_utils import get_cation_formula

def calculate_formula_molar_mass(formula_str):
    try:
        parsed_entity = periodictable.formula(formula_str)
        return float(parsed_entity.mass)
    except ValueError as ve:
        return None


def get_molar_mass_of_salt(salt_formula_str):
    match = re.match(r"([A-Z][a-zA-Z0-9_]*)(Cl|Br|I)(\d*)$", salt_formula_str.strip())
    if match:
        cation_name = match.group(1)
        halide_symbol = match.group(2)
        halide_index_str = match.group(3)
        halide_count = int(halide_index_str) if halide_index_str else 1
        cation_formula = get_cation_formula(cation_name)
        cation_mass = calculate_formula_molar_mass(cation_formula)
        halide_mass = calculate_formula_molar_mass(halide_symbol)
        total_mass = cation_mass + (halide_count * halide_mass)
        return total_mass
    else:
        # такого в целом при корректном заполнении базы данных быть не может
        return calculate_formula_molar_mass(salt_formula_str)

def get_salt_formula(cation_name, halide, valence):
    return f"{cation_name}{halide}" if valence == "1" else f"{cation_name}{halide}{valence}"
