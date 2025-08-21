def generate_reaction_equations_display(
    phase_components_for_formula,
    phase_anion_config_for_formula,
    phase_template_sites_info_for_formula,
    calculation_results,
    sorted_equation_keys = None,
):
    output_lines = []
    product_formula_str = "[Формула продукта?]"

    product_formula_str = calculation_results["product_formula_display"]

    equations_data_map = calculation_results.get("equations", {})
    if not equations_data_map:
        return "Нет данных по уравнениям."

    input_summary = calculation_results.get("input_summary", {})

    main_solvents_input: List[Dict[str, str]] = input_summary.get(
        "main_solvents_mix_input", []
    )
    antisolvents_input: List[Dict[str, str]] = input_summary.get(
        "antisolvents_mix_input", []
    )
    v_antisolvent_ml_input: Decimal = input_summary.get(
        "V_antisolvent_ml_input", Decimal("0.0")
    )
    v_main_solution_ml_input: Decimal = input_summary.get(
        "V_solution_ml", Decimal("0.0")
    )

    keys_to_iterate: List[str] = (
        sorted_equation_keys
        if sorted_equation_keys is not None
        else sorted(
            equations_data_map.keys(),
            key=lambda k: (
                int(k.split(" ")[1])
                if k.startswith("Equation ")
                and len(k.split(" ")) > 1
                and k.split(" ")[1].isdigit()
                else 9999
            ),
        )
    )

    if not keys_to_iterate:
        return "Не найдено уравнений для отображения.\n"

    for eq_key in keys_to_iterate:
        eq_data = equations_data_map.get(eq_key)
        if not isinstance(eq_data, dict) or not eq_data.get("condition_met", False):
            continue

        coefficients_map_for_eq = eq_data.get("coefficients_detailed")
        if not isinstance(coefficients_map_for_eq, dict) or not coefficients_map_for_eq:
            output_lines.append(
                f"{eq_key} ({eq_data.get('description', 'N/A')}): [Ошибка: нет коэфф.]  ⟶  {product_formula_str}\n"
            )
            continue

        reactants_parts_str_list: List[str] = []
        sorted_salt_keys_for_eq_display = sorted(
            coefficients_map_for_eq.keys(), key=sort_key_salt
        )

        for salt_formula in sorted_salt_keys_for_eq_display:
            coeff_val_decimal = coefficients_map_for_eq.get(salt_formula)
            if (
                coeff_val_decimal is None
                or abs(coeff_val_decimal) < constants.ZERO_THRESHOLD
            ):
                continue
            formatted_coeff_str = format_coefficient(coeff_val_decimal, precision=3)
            if formatted_coeff_str is None:
                continue
            coeff_display_part = (
                f"{formatted_coeff_str} " if formatted_coeff_str.strip() else ""
            )
            reactants_parts_str_list.append(f"{coeff_display_part}{salt_formula}")

        total_cost_val = eq_data.get(
            "total_cost_final_k"
        )  # Общая стоимость в target_currency
        cost_str_part = ""

        if total_cost_val is not None:
            cost_display_parts = []
            if target_currency == "USD":
                cost_display_parts.append(f"{total_cost_val:.2f} USD")
                if usd_to_rub_rate:
                    rub_equiv = (total_cost_val * usd_to_rub_rate).quantize(
                        Decimal("0.01"), ROUND_HALF_UP
                    )
                    cost_display_parts.append(f"{rub_equiv:.2f} RUB")
            elif target_currency == "RUB":
                cost_display_parts.append(f"{total_cost_val:.2f} RUB")
                if usd_to_rub_rate:
                    usd_equiv = (total_cost_val / usd_to_rub_rate).quantize(
                        Decimal("0.01"), ROUND_HALF_UP
                    )
                    cost_display_parts.append(f"{usd_equiv:.2f} USD")
            else:  # На случай, если target_currency не USD/RUB, хотя это не должно происходить
                cost_display_parts.append(f"{total_cost_val:.2f} {target_currency}")

            cost_str_part = f"  (Общ. стоимость: {' / '.join(cost_display_parts)})"

        elif (
            eq_data.get("num_reagents_with_cost", 0) < eq_data.get("num_reagents", 0)
            or eq_data.get("num_solvents_with_cost", 0)
            < (
                len(main_solvents_input)
                + (len(antisolvents_input) if v_antisolvent_ml_input > 0 else 0)
            )
        ) and (
            eq_data.get("num_reagents", 0) > 0
            or (
                len(main_solvents_input)
                + (len(antisolvents_input) if v_antisolvent_ml_input > 0 else 0)
            )
            > 0
        ):
            cost_str_part = "  (Общ. стоимость: N/A - не все цены известны)"

        solvent_info_str_part = ""
        main_solvent_details_parts = []
        if main_solvents_input and v_main_solution_ml_input > Decimal("0"):
            for ms_info in main_solvents_input:
                ms_sym = ms_info.get("symbol")
                ms_fr_str = ms_info.get("fraction")
                try:
                    ms_fr_dec = Decimal(ms_fr_str)
                    ms_vol = v_main_solution_ml_input * ms_fr_dec
                    if ms_vol > constants.ZERO_THRESHOLD:
                        formatted_frac = format_coefficient(ms_fr_dec, precision=2)
                        main_solvent_details_parts.append(
                            f"{ms_sym}{formatted_frac if formatted_frac else ''} [{ms_vol:.2f}мл]"
                        )
                except:
                    main_solvent_details_parts.append(f"{ms_sym}({ms_fr_str})")
        if main_solvent_details_parts:
            solvent_info_str_part += (
                f" | Раств-ль: {', '.join(main_solvent_details_parts)}"
            )

        antisolvent_details_parts = []
        if antisolvents_input and v_antisolvent_ml_input > Decimal("0"):
            for as_info in antisolvents_input:
                as_sym = as_info.get("symbol")
                as_fr_str = as_info.get("fraction")
                try:
                    as_fr_dec = Decimal(as_fr_str)
                    as_vol = v_antisolvent_ml_input * as_fr_dec
                    if as_vol > constants.ZERO_THRESHOLD:
                        formatted_frac = format_coefficient(as_fr_dec, precision=2)
                        antisolvent_details_parts.append(
                            f"{as_sym}{formatted_frac if formatted_frac else ''} [{as_vol:.2f}мл]"
                        )
                except:
                    antisolvent_details_parts.append(f"{as_sym}({as_fr_str})")
        if antisolvent_details_parts:
            solvent_info_str_part += f" | Антираств-ль ({v_antisolvent_ml_input:.2f}мл общ.): {', '.join(antisolvent_details_parts)}"

        if reactants_parts_str_list:
            reactants_str = " + ".join(reactants_parts_str_list)
            output_lines.append(
                f"{eq_key} ({eq_data.get('description', 'N/A')}): {reactants_str}  ⟶  {product_formula_str}{cost_str_part}{solvent_info_str_part}\n"
            )
        else:
            output_lines.append(
                f"{eq_key} ({eq_data.get('description', 'N/A')}): [Нет знач. реагентов]  ⟶  {product_formula_str}{cost_str_part}{solvent_info_str_part}\n"
            )

    return (
        "".join(output_lines) if output_lines else "Не найдено применимых уравнений.\n"
    )


def format_results_mass_table(
    calculation_results: Dict[str, Any],
    sorted_equation_keys: Optional[List[str]] = None,
    authoritative_salt_list: Optional[List[str]] = None,
) -> str:
    if not calculation_results or not calculation_results.get("equations"):
        return "Нет данных для таблицы масс и цен."

    equations_data_map = calculation_results["equations"]
    target_currency = calculation_results.get("input_summary", {}).get(
        "target_currency_for_costs", "USD"
    )
    currency_symbol = (
        "$" if target_currency == "USD" else "₽"
    )  # Для таблицы пока одна валюта

    keys_to_process: List[str] = (
        sorted_equation_keys
        if sorted_equation_keys is not None
        else sorted(
            equations_data_map.keys(),
            key=lambda k: (
                int(k.split(" ")[1])
                if k.startswith("Equation ")
                and len(k.split(" ")) > 1
                and k.split(" ")[1].isdigit()
                else 9999
            ),
        )
    )

    valid_equations_for_table: List[str] = []
    for eq_key in keys_to_process:
        eq_data = equations_data_map.get(eq_key)
        if (
            isinstance(eq_data, dict)
            and eq_data.get("condition_met", False)
            and eq_data.get("coefficients_detailed")
        ):
            valid_equations_for_table.append(eq_key)

    if not valid_equations_for_table:
        return f"\nТаблица Масс (г) и Общей Стоимости ({currency_symbol}):\nНет валидных уравнений для отображения."

    if authoritative_salt_list is None:
        logger.warning(
            "format_results_mass_table: authoritative_salt_list не предоставлен. Формирую из уравнений."
        )
        temp_header_salts_set: set = set()
        for eq_key_fb in valid_equations_for_table:
            eq_data_fb = equations_data_map.get(eq_key_fb)
            if isinstance(eq_data_fb, dict):
                coeffs_dict_fb = eq_data_fb.get("coefficients_detailed", {})
                for salt_fb, coeff_val_fb in coeffs_dict_fb.items():
                    if (
                        isinstance(salt_fb, str)
                        and coeff_val_fb is not None
                        and abs(coeff_val_fb) > constants.ZERO_THRESHOLD
                    ):
                        temp_header_salts_set.add(salt_fb)
        header_salts_sorted_list: List[str] = sorted(
            list(temp_header_salts_set), key=sort_key_salt
        )
    else:
        header_salts_sorted_list = authoritative_salt_list

    if not header_salts_sorted_list:
        return f"\nТаблица Масс (г) и Общей Стоимости ({currency_symbol}):\nНет солей для отображения в таблице."

    cell_width = app_config.TABLE_CELL_WIDTH
    header_cell_format = app_config.TABLE_CELL_FORMAT
    first_col_width = 10

    cost_column_header = f"Ст-ть({currency_symbol})"[:cell_width]
    header_parts = ["{:<{width}}".format("Уравнение", width=first_col_width)]
    for salt_in_header in header_salts_sorted_list:
        display_salt_name = salt_in_header[:cell_width]
        header_parts.append(header_cell_format.format(display_salt_name))
    header_parts.append(header_cell_format.format(cost_column_header))
    header_line_str = "".join(header_parts)
    table_separator_str = "=" * len(header_line_str)

    output_lines: List[str] = [
        f"\nТаблица Масс (г) и Общей Стоимости ({currency_symbol}):",
        table_separator_str,
        header_line_str,
        table_separator_str,
    ]

    for eq_key in valid_equations_for_table:
        eq_data = equations_data_map[eq_key]
        mass_dict_final = eq_data.get("masses_g_final_k", {})
        total_cost_final_val = eq_data.get("total_cost_final_k")

        eq_num_str = eq_key.split(" ")[1] if eq_key.startswith("Equation ") else eq_key
        row_name_str = f"Eq {eq_num_str}"[:first_col_width]
        row_str_parts = ["{:<{width}}".format(row_name_str, width=first_col_width)]

        for salt_in_header in header_salts_sorted_list:
            mass_val = mass_dict_final.get(salt_in_header)
            is_error_cell = mass_val == app_config.MASS_ERROR_MARKER
            row_str_parts.append(
                format_value_for_cell(
                    mass_val, is_error=is_error_cell, is_cost_value=False
                )
            )

        row_str_parts.append(
            format_value_for_cell(
                total_cost_final_val,
                is_error=False,
                is_cost_value=True,
                target_currency_symbol=currency_symbol,
            )
        )
        output_lines.append("".join(row_str_parts))

    output_lines.append(table_separator_str)
    return "\n".join(output_lines)


def format_geometry_factors(factors_dict: Optional[Dict[str, Any]]) -> str:
    if not factors_dict:
        return "Геометрические факторы: Н/Д"
    if "error" in factors_dict:
        return f"Геометрические факторы: [{factors_dict['error']}]"

    parts = []
    t_val = factors_dict.get("t")
    if t_val == "N/A":
        parts.append("t = N/A")
    elif isinstance(t_val, Decimal):
        parts.append(f"t = {t_val:.3f}")
    elif t_val is None and ("mu" in factors_dict or "mu_prime" in factors_dict):
        parts.append("t = ?")

    mu_val = factors_dict.get("mu")
    mu_p_val = factors_dict.get("mu_prime")
    mu_dp_val = factors_dict.get("mu_double_prime")

    if isinstance(mu_val, Decimal):
        parts.append(f"μ = {mu_val:.3f}")
    elif mu_val is None and "t" in factors_dict and factors_dict.get("t") != "N/A":
        parts.append("μ = ?")

    if mu_p_val is not None:
        mu_prime_str = f"{mu_p_val:.3f}" if isinstance(mu_p_val, Decimal) else "?"
        parts.append(f"μ' = {mu_prime_str}")

    if mu_dp_val is not None:
        mu_double_prime_str = (
            f"{mu_dp_val:.3f}" if isinstance(mu_dp_val, Decimal) else "?"
        )
        parts.append(f"μ'' = {mu_double_prime_str}")

    if not parts:
        return "Геометрические факторы: Н/Д"
    else:
        return "Геометрические факторы: " + ", ".join(parts)