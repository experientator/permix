import re
import periodictable
from analysis.database_utils import get_cation_formula
from analysis.geometry_calculator import show_error
import analysis.constants as constants

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

def calculate_target_product_moles(c_solution_molar, v_solution_ml):
    n_perovskite_target_moles = c_solution_molar * (v_solution_ml / 1000.0)
    return n_perovskite_target_moles

def calculate_target_anion_moles(anions, total_anion_stoich):
    """
    Рассчитывает целевые моли каждого аниона в продукте на единицу формулы продукта.
    """
    target_moles= {
        hal: 0.0 for hal in ["Cl", "Br", "I"]
    }

    current_sum_fractions = 0
    calculated_total_moles_check = 0.0

    for item in anions:
        current_sum_fractions += float(item.get("fraction"))
        hal_symbol = item["symbol"]
        fraction = float(item["fraction"])
        moles_of_hal = int(total_anion_stoich) * fraction

        target_moles[hal_symbol] = (
            moles_of_hal
        )
        calculated_total_moles_check += moles_of_hal

    relative_tolerance = 1e-7
    absolute_tolerance = 1e-9  # Допуск для проверки суммы молей
    max_abs_val = max(
        abs(calculated_total_moles_check),
        abs(total_anion_stoich),
        1.0,
    )
    diff_check = abs(calculated_total_moles_check - total_anion_stoich)

    if diff_check > max(absolute_tolerance, relative_tolerance * max_abs_val):
        show_error(
            f"MC_UTILS: Итоговая сумма молей анионов ({calculated_total_moles_check:.6f}) "
            f"не соответствует целевой ({total_anion_stoich:.6f}) после расчета. "
            # ИЗМЕНЕНО ЗДЕСЬ:
            f"Разница: {float(diff_check):.2E}"
        )
    print(target_moles)
    return target_moles

def determine_base_anion_for_rigid_cations(anions_moles):
    """
    Определяет базовый анион для "жестких" катионов.
    """
    non_zero_halides_with_moles = {
        hal: float(moles)
        for hal, moles in anions_moles.items()
    }

    max_moles = max(non_zero_halides_with_moles.values())
    candidate_halides = [
        h_symbol
        for h_symbol, h_moles in non_zero_halides_with_moles.items()
        if h_moles == max_moles
    ]

    if len(candidate_halides) > 1:
        halide_order_map = {hal: i for i, hal in enumerate(constants.halides())}
        candidate_halides.sort(key=lambda h_cand: halide_order_map.get(h_cand, 99))

    base_X_rigid = candidate_halides[0]

    return base_X_rigid

def round_cations(cations_site):
    return "(" + cations_site + ")"

def generate_formula_string(cations_config,
                            anions_config,
                            anion_stoichiometry):
    SITE_DISPLAY_ORDER = [
        "a_site",
        "spacer",
        "b_site",
        "b_double",
        "anion"
    ]

    cations_by_site = {site_type: [] for site_type in SITE_DISPLAY_ORDER}

    for cation in cations_config:
        site_type = cation["structure_type"]
        if site_type in cations_by_site:
            cations_by_site[site_type].append(cation)

    full_cation_formula = ""
    site_cation_parts = ""
    round_flag = 0
    site_stoich: str
    anion_flag = 0

    for site_key_ordered in SITE_DISPLAY_ORDER:
        if site_key_ordered == "anion":
            components_on_this_site = anions_config
            anion_flag = 1
        else:
            components_on_this_site = cations_by_site[site_key_ordered]
        components_on_this_site.sort(key=lambda x: float(x["fraction"]), reverse=True)
        if not components_on_this_site:
            continue
        for component in components_on_this_site:
            if anion_flag == 1:
                site_stoich = str(anion_stoichiometry)
            else:
                site_stoich = str(component["stoichiometry"])
            if float(component["fraction"]) == 1:
                site_cation_parts += component["symbol"]
                round_flag = 1
            else:
                site_cation_parts += component["symbol"]
                site_cation_parts += str(round(float(component["fraction"]), 3))
        if round_flag == 0:
            site_cation_parts = round_cations(site_cation_parts)
        full_cation_formula += site_cation_parts
        site_cation_parts = ""
        round_flag = 0
        if float(site_stoich) != 1.0:
            full_cation_formula += str(int(float(site_stoich)))

    return full_cation_formula