import sqlite3
from decimal import Decimal

def get_templates_list():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT DISTINCT name FROM Phase_templates ORDER BY dimensionality")
    values = [row[0] for row in cursor.fetchall()]

    conn.close()
    return values

def get_template_id(name):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM Phase_templates WHERE name = ?", (name,))
    id_phase = cursor.fetchone()
    conn.close()
    return int(id_phase[0])

def calculate_target_product_moles(c_solution_molar, v_solution_ml):
    """Рассчитывает общее количество молей продукта."""
    n_perovskite_target_moles = c_solution_molar * (v_solution_ml / Decimal("1000.0"))
    return n_perovskite_target_moles


def prepare_active_cations_details(cation_components_map):
    """
    Подготавливает список деталей активных катионов для расчета.
    Предполагается, что 'actual_stoichiometry_in_product' уже Decimal.
    """
    active_cations_details = []
    for site_name, components_list_on_site in cation_components_map.items():
        for comp_data in components_list_on_site:
            symbol = comp_data.get("symbol")
            actual_stoich = comp_data.get(
                "actual_stoichiometry_in_product"
            )
            valence = comp_data.get("valence")
            active_cations_details.append(
                {
                    "symbol": symbol,
                    "valence": valence,
                    "stoich_in_product_unit": actual_stoich,
                    "site": site_name,
                }
            )

    active_cations_details.sort(key=lambda x: (x["site"], x["symbol"]))
    return active_cations_details


def calculate_target_anion_moles_per_formula_unit(anion_config_from_gui, total_anion_stoich_product):
    """
    Рассчитывает целевые моли каждого аниона в продукте на единицу формулы продукта.
    """
    target_moles = {
        hal: Decimal("0.0") for hal in constants.get_halides()
    }
    anion_mix_list = anion_config_from_gui.get("anion_mix", [])
    current_sum_fractions = Decimal("0.0")
    valid_mix_data_for_calc = []
    halides_in_mix_set = set()

    for item in anion_mix_list:
        hal_symbol = item.get("symbol")
        fraction_decimal = item.get("fraction")  # Ожидается Decimal

        halides_in_mix_set.add(hal_symbol)
        if fraction_decimal > constants.ZERO_THRESHOLD:
            current_sum_fractions += fraction_decimal
            valid_mix_data_for_calc.append(
                {"symbol": hal_symbol, "fraction": fraction_decimal}
            )
    SUM_TARGET = Decimal("1.0")
    SUM_TOLERANCE_ANION_FRACTIONS = Decimal("0.0015")  # Допуск

    if abs(current_sum_fractions - SUM_TARGET) > SUM_TOLERANCE_ANION_FRACTIONS:
        normalization_factor = SUM_TARGET / current_sum_fractions
        temp_normalized_sum = Decimal("0.0")
        for item_data in valid_mix_data_for_calc:
            item_data["fraction"] *= normalization_factor
            temp_normalized_sum += item_data["fraction"]

    calculated_total_moles_check = Decimal("0.0")
    for item_data in valid_mix_data_for_calc:
        hal_symbol = item_data["symbol"]
        normalized_fraction = item_data["fraction"]
        moles_of_hal = total_anion_stoich_product * normalized_fraction

        target_moles[hal_symbol] = (
            moles_of_hal  # Не должно быть символов не из constants.HALIDES
        )
        calculated_total_moles_check += moles_of_hal

    relative_tolerance = Decimal("1e-7")
    absolute_tolerance = Decimal("1e-9")  # Допуск для проверки суммы молей
    max_abs_val = max(
        abs(calculated_total_moles_check),
        abs(total_anion_stoich_product),
        Decimal("1.0"),
    )
    diff_check = abs(calculated_total_moles_check - total_anion_stoich_product)

    quantizer_moles = Decimal("0.000001")  # 6 знаков после запятой
    for hal_symbol_final in target_moles:
        target_moles[hal_symbol_final] = target_moles[hal_symbol_final].quantize(
            quantizer_moles, rounding=ROUND_HALF_UP
        )
    return target_moles


def determine_base_anion_for_rigid_cations(target_anion_moles_map):
    """
    Определяет базовый анион для "жестких" катионов.
    """
    all_halides_list = constants.get_halides()
    non_zero_halides_with_moles = {
        hal: moles
        for hal, moles in target_anion_moles_map.items()
        if moles > constants.ZERO_THRESHOLD and hal in all_halides_list
    }
    base_X_rigid: str
    max_moles = max(non_zero_halides_with_moles.values())
    candidate_halides = [
        h_symbol
        for h_symbol, h_moles in non_zero_halides_with_moles.items()
        # Сравнение Decimal должно быть точным, если max_moles взято из тех же значений
        if h_moles == max_moles
    ]

    if len(candidate_halides) > 1:
        halide_order_map = {hal: i for i, hal in enumerate(all_halides_list)}
        candidate_halides.sort(key=lambda h_cand: halide_order_map.get(h_cand, 99))
    base_X_rigid = candidate_halides[0]
    return base_X_rigid