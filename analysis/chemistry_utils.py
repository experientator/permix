import re
import periodictable
from analysis.database_utils import get_cation_formula
from analysis.geometry_calculator import show_error
import constants

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

def generate_formula_string(cations_config,
                            anions_config,
                            template_sites_info,
                            anion_stoichiometry):
    SITE_DISPLAY_ORDER = [
        "a_site",
        "spacer",
        "b_site",
        "b_double",
    ]
    full_cation_formula_parts = []

    cations_by_site = {site_type: [] for site_type in SITE_DISPLAY_ORDER}

    for cation in cations_config:
        site_type = cation["structure_type"]
        if site_type in cations_by_site:
            cations_by_site[site_type].append(cation)

    full_cation_formula_parts = []

    for site_key_ordered in SITE_DISPLAY_ORDER:
        components_on_this_site = cations_by_site[site_key_ordered]
        if not components_on_this_site:
            continue

            site_cation_parts_str_list = []
            base_stoich_for_this_site_from_template = 1.0
            site_info_from_tpl = template_sites_info.get(site_key_ordered)

            if site_info_from_tpl and isinstance(site_info_from_tpl, dict):
                base_stoich_val = site_info_from_tpl.get("base_stoichiometry", "1.0")

            needs_site_parentheses = (len(components_on_this_site) > 1) or (
                len(components_on_this_site) == 1
                and abs(base_stoich_for_this_site_from_template - 1.0)
                > 1e-9
            )

            for component_data in components_on_this_site:
                symbol = component_data.get("symbol")
                fraction_on_site_dec = component_data.get("fraction_on_site")

                formatted_fraction_str = format_coefficient(
                    fraction_on_site_dec, precision=2
                )
                site_cation_parts_str_list.append(
                    f"{symbol}{formatted_fraction_str if formatted_fraction_str else ''}"
                )

            if site_cation_parts_str_list:
                concatenated_site_cations_str = "".join(site_cation_parts_str_list)
                if needs_site_parentheses:
                    concatenated_site_cations_str = f"({concatenated_site_cations_str})"

                formatted_site_stoich_str = format_coefficient(
                    base_stoich_for_this_site_from_template, precision=2
                )
                if formatted_site_stoich_str:
                    concatenated_site_cations_str += formatted_site_stoich_str
                full_cation_formula_parts.append(concatenated_site_cations_str)

    full_cation_str = "".join(full_cation_formula_parts)
    if not full_cation_str:
        full_cation_str = "[Катионы?]"

    anion_formula_part_str = ""

    if len(anions_config) == 1:
        anion_formula_part_str = anions_config[0]["symbol"]
    else:
        halide_order_map = {h: i for i, h in enumerate(constants.halides)}
        anions_config.sort(
            key=lambda x: halide_order_map.get(x["symbol"], 99)
        )
        anion_parts_list = []
        for anion_data in anions_config:
            symbol = anion_data["symbol"]
            fraction = anion_data["fraction"]
            formatted_fraction_str = format_coefficient(fraction, precision=2)
            anion_parts_list.append(
                f"{symbol}{formatted_fraction_str if formatted_fraction_str else ''}"
            )
        anion_formula_part_str = f"({''.join(anion_parts_list)})"

    formatted_total_anion_stoich_str = format_coefficient(
        anion_stoichiometry, precision=2
    )
    if formatted_total_anion_stoich_str:
        anion_formula_part_str += formatted_total_anion_stoich_str

    final_formula = f"{full_cation_str}{anion_formula_part_str}"
    logger.info(f"DISPLAY_FORMATTERS: Сгенерированная формула: {final_formula}")
    return final_formula