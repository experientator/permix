import src.utils.constants as constants
import re
from src.utils.database_utils import get_cation_list_by_key
import decimal
from decimal import Decimal, ROUND_HALF_UP

def format_value_for_cell(
    value,
    is_error = False,
    is_cost_value = False):
    cell_width = constants.TABLE_CELL_WIDTH
    final_cell_format = constants.TABLE_CELL_FORMAT
    try:
        value_dec = Decimal(str(value))
    except (decimal.InvalidOperation, TypeError, ValueError):
        error_text = "Inv.Val"
        return final_cell_format.format(error_text[:cell_width])

    precision = 4

    if Decimal("0") < abs(value_dec) < Decimal("1e-4"):
        precision = 5
    elif abs(value_dec) >= Decimal("10000"):
        precision = 2
    elif abs(value_dec) >= Decimal("100"):
        precision = 3

    if abs(value_dec) >= Decimal("1000") and not is_cost_value:
        int_candidate = value_dec.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        if abs(int_candidate - value_dec) < Decimal("1e-3"):
            formatted_int_str = format(int_candidate, ".0f")
            if len(formatted_int_str) <= cell_width:
                return final_cell_format.format(formatted_int_str)

    quantizer = Decimal("1e-" + str(precision))
    rounded_dec = value_dec.quantize(quantizer, rounding=ROUND_HALF_UP)
    formatted_val_str = f"{rounded_dec:.{precision}f}".rstrip("0").rstrip(".")
    if formatted_val_str == "-0":
        formatted_val_str = "0"
    if not formatted_val_str:
        formatted_val_str = "0"

    if len(formatted_val_str) > cell_width:
        sci_precision = 2
        temp_sci_formatted = ""
        while sci_precision >= 0:
            try:
                sci_formatted_candidate = format(value_dec, f".{sci_precision}E")
                sci_formatted_candidate = sci_formatted_candidate.replace(
                    "E+0", "E+"
                ).replace("E-0", "E-")
                if len(sci_formatted_candidate) <= cell_width:
                    temp_sci_formatted = sci_formatted_candidate
                    break
                elif not temp_sci_formatted or len(sci_formatted_candidate) < len(
                    temp_sci_formatted
                ):
                    temp_sci_formatted = sci_formatted_candidate
                sci_precision -= 1
            except Exception:
                temp_sci_formatted = "Overflow"
                break
        if temp_sci_formatted and len(temp_sci_formatted) <= cell_width:
            formatted_val_str = temp_sci_formatted
        elif temp_sci_formatted:
            formatted_val_str = temp_sci_formatted[: cell_width - 1] + "~"
        else:
            formatted_val_str = formatted_val_str[: cell_width - 1] + "~"

    final_output = formatted_val_str[:cell_width]
    return final_cell_format.format(final_output)

def sort_key_salt(salt_formula_str):
    match = re.match(r"([A-Z][a-zA-Z0-9_]*)(Cl|Br|I)(\d*)$", salt_formula_str.strip())

    cation_key = match.group(1)
    halide = match.group(2)
    halide_index_str = match.group(3)
    valence = int(halide_index_str) if halide_index_str else 1

    category_priority = 2
    if cation_key in get_cation_list_by_key("a_site_val_1"):
        category_priority = 0
    elif cation_key in get_cation_list_by_key(
            "spacer_val_1"
    ) or cation_key in get_cation_list_by_key("spacer_val_2"):
        category_priority = 1

    halide_priority = {"Cl": 0, "Br": 1, "I": 2}.get(halide, 9)
    return (category_priority, valence, cation_key, halide_priority)

def generate_reaction_equations_display(
    calculation_results,
    sorted_equation_keys = None,
):
    ("adf1", "Inv.Val", "[Формула продукта?]"),
    ("adf2", "Fractions", "Нет данных по уравнениям"),
    ("act_err3", "Fraction summ", "Сумма долей"),
    ("act_err4", "must be equal to 1", "должна быть равна 1"),
    output_lines = []
    equation_formulas = list()
    product_formula_str = "[Формула продукта?]"

    product_formula_str = calculation_results["product_formula_display"]

    equations_data_map = calculation_results.get("equations", {})
    if not equations_data_map:
        return "Нет данных по уравнениям."

    input_summary = calculation_results.get("input_summary", {})

    main_solvents_input = input_summary.get(
        "main_solvents_mix_input", []
    )
    antisolvents_input = input_summary.get(
        "antisolvents_mix_input", []
    )
    v_antisolvent_ml_input = input_summary.get(
        "V_antisolvent_ml_input", 0.0
    )
    v_main_solution_ml_input = input_summary.get(
        "V_solution_ml", 0.0
    )

    keys_to_iterate = (
        sorted_equation_keys
        if sorted_equation_keys is not None
        else sorted(
            equations_data_map.keys(),
            key=lambda k: (
                int(k.split(" ")[1])
                if k.startswith("Equation ")
                and k.split(" ")[1].isdigit()
                else 9999
            ),
        )
    )

    if not keys_to_iterate:
        return "Не найдено уравнений для отображения.\n"

    solvent_info_str_part = ""
    main_solvent_details_parts = []
    if main_solvents_input and float(v_main_solution_ml_input) > 0:
        for ms_info in main_solvents_input:
            ms_sym = ms_info.get("symbol")
            ms_fr = float(ms_info.get("fraction"))
            try:
                ms_vol = v_main_solution_ml_input * ms_fr
                main_solvent_details_parts.append(
                    f"{ms_sym}{ms_fr if ms_fr else ''} [{ms_vol:.2f}мл]"
                )
            except:
                main_solvent_details_parts.append(f"{ms_sym}({ms_fr})")
    if main_solvent_details_parts:
        solvent_info_str_part += (
            f" | Раств-ль: {', '.join(main_solvent_details_parts)}"
        )

    antisolvent_details_parts = []
    if antisolvents_input and float(v_antisolvent_ml_input) > 0:
        for as_info in antisolvents_input:
            as_sym = as_info.get("symbol")
            as_fr = float(as_info.get("fraction"))
            try:
                as_vol = v_antisolvent_ml_input * as_fr
                antisolvent_details_parts.append(
                    f"{as_sym}{as_fr if as_fr else ''} [{as_vol:.2f}мл]"
                )
            except:
                antisolvent_details_parts.append(f"{as_sym}({as_fr})")

    if antisolvent_details_parts:
        solvent_info_str_part += f" | Антираств-ль ({v_antisolvent_ml_input:.2f}мл общ.): {', '.join(antisolvent_details_parts)}"

    for eq_key in keys_to_iterate:
        eq_data = equations_data_map.get(eq_key)
        if not isinstance(eq_data, dict) or not eq_data.get("condition_met", False):
            continue

        coefficients_map_for_eq = eq_data.get("coefficients_detailed")
        reactants_parts_str_list = []
        sorted_salt_keys_for_eq_display = sorted(
            coefficients_map_for_eq.keys(), key=sort_key_salt
        )

        for salt_formula in sorted_salt_keys_for_eq_display:
            coeff_val = coefficients_map_for_eq.get(salt_formula)
            if (
                coeff_val is None
            ):
                continue
            if coeff_val is None:
                continue
            coeff_display_part = (
                f"{coeff_val} "
            )
            reactants_parts_str_list.append(f"{coeff_display_part}{salt_formula}")


        if reactants_parts_str_list:
            reactants_str = " + ".join(reactants_parts_str_list)
            equation_formulas.append(f"{reactants_str}  ⟶  {product_formula_str}")
            output_lines.append(
                f"{eq_key} ({eq_data.get('description', 'N/A')}): {reactants_str}  ⟶  {product_formula_str}{solvent_info_str_part}\n"
            )
    return (
        "".join(output_lines) if output_lines else "Не найдено применимых уравнений.\n", equation_formulas
    )

def format_results_mass_table(
    calculation_results,
    sorted_equation_keys = None,
    authoritative_salt_list = None):
    if not calculation_results or not calculation_results.get("equations"):
        return "Нет данных для таблицы масс"

    equations_data_map = calculation_results["equations"]

    keys_to_process = (
        sorted_equation_keys
        if sorted_equation_keys is not None
        else sorted(
            equations_data_map.keys(),
            key=lambda k: (
                int(k.split(" ")[1])
                if k.startswith("Equation ")
                and k.split(" ")[1].isdigit()
                else 9999
            ),
        )
    )

    valid_equations_for_table = []
    for eq_key in keys_to_process:
        eq_data = equations_data_map.get(eq_key)
        if (
            isinstance(eq_data, dict)
            and eq_data.get("condition_met", False)
            and eq_data.get("coefficients_detailed")
        ):
            valid_equations_for_table.append(eq_key)

    if not valid_equations_for_table:
        return f"\nТаблица Масс (г)):\nНет валидных уравнений для отображения."

    if authoritative_salt_list is None:
        temp_header_salts_set: set = set()
        for eq_key_fb in valid_equations_for_table:
            eq_data_fb = equations_data_map.get(eq_key_fb)
            if isinstance(eq_data_fb, dict):
                coeffs_dict_fb = eq_data_fb.get("coefficients_detailed", {})
                for salt_fb, coeff_val_fb in coeffs_dict_fb.items():
                    if (
                        isinstance(salt_fb, str)
                        and coeff_val_fb is not None
                    ):
                        temp_header_salts_set.add(salt_fb)
        header_salts_sorted_list = sorted(
            list(temp_header_salts_set), key=sort_key_salt
        )
    else:
        header_salts_sorted_list = authoritative_salt_list

    if not header_salts_sorted_list:
        return f"\nТаблица Масс (г):\nНет солей для отображения в таблице."

    cell_width = constants.TABLE_CELL_WIDTH
    header_cell_format = constants.TABLE_CELL_FORMAT
    first_col_width = 10

    header_parts = ["{:<{width}}".format("Уравнение", width=first_col_width)]
    for salt_in_header in header_salts_sorted_list:
        display_salt_name = salt_in_header[:cell_width]
        header_parts.append(header_cell_format.format(display_salt_name))
    header_line_str = "".join(header_parts)
    table_separator_str = "=" * len(header_line_str)

    output_lines = [
        f"\nТаблица Масс (г):",
        table_separator_str,
        header_line_str,
        table_separator_str,
    ]

    for eq_key in valid_equations_for_table:
        eq_data = equations_data_map[eq_key]
        mass_dict_final = eq_data.get("masses_g_final_k", {})

        eq_num_str = eq_key.split(" ")[1] if eq_key.startswith("Equation ") else eq_key
        row_name_str = f"Eq {eq_num_str}"[:first_col_width]
        row_str_parts = ["{:<{width}}".format(row_name_str, width=first_col_width)]

        for salt_in_header in header_salts_sorted_list:
            mass_val = mass_dict_final.get(salt_in_header)
            is_error_cell = mass_val == constants.MASS_ERROR_MARKER
            row_str_parts.append(
                format_value_for_cell(
                    mass_val, is_error=is_error_cell, is_cost_value=False
                )
            )

        output_lines.append("".join(row_str_parts))

    output_lines.append(table_separator_str)
    return "\n".join(output_lines)

def format_geometry_factors(factors_dict):
    if not factors_dict:
        return "Геометрические факторы: Н/Д"
    if "error" in factors_dict:
        return f"Геометрические факторы: [{factors_dict['error']}]"

    parts = []
    t_val = factors_dict.get("t")
    if t_val == "N/A":
        parts.append("t = N/A")
    elif isinstance(t_val, str):
        parts.append(f"t = {t_val:.3f}")
    elif t_val is None and ("mu" in factors_dict or "mu_prime" in factors_dict):
        parts.append("t = ?")

    mu_val = factors_dict.get("mu")
    mu_p_val = factors_dict.get("mu_prime")
    mu_dp_val = factors_dict.get("mu_double_prime")

    if isinstance(mu_val, str):
        parts.append(f"μ = {mu_val:.3f}")
    elif mu_val is None and "t" in factors_dict and factors_dict.get("t") != "N/A":
        parts.append("μ = ?")

    if mu_p_val is not None:
        mu_prime_str = f"{mu_p_val:.3f}" if isinstance(mu_p_val, str) else "?"
        parts.append(f"μ' = {mu_prime_str}")

    if mu_dp_val is not None:
        mu_double_prime_str = (
            f"{mu_dp_val:.3f}" if isinstance(mu_dp_val, str) else "?"
        )
        parts.append(f"μ'' = {mu_double_prime_str}")

    if not parts:
        return "Геометрические факторы: Н/Д"
    else:
        return "Геометрические факторы: " + ", ".join(parts)