def format_summary_text(
    equation_data,
    input_summary_data,
    geometry_factors_data,
    product_formula_display):
    """
    Формирует текстовую сводку для указанного уравнения.
    """
    lines = []

    try:
        # 1. Номер уравнения
        eq_num = equation_data.get("eq_key_numeric", "?")
        lines.append(f"Уравнение {eq_num}")

        # 2. Состав
        lines.append(product_formula_display)

        # 3. Геометрические факторы
        geom_factors_str = display_formatters.format_geometry_factors(
            geometry_factors_data
        )
        lines.append(geom_factors_str)  # format_geometry_factors уже добавляет префикс

        # 4. Концентрация
        c_molar_str = input_summary_data.get("C_solution_molar", "?")
        lines.append(f"C = {c_molar_str} [М]")

        # 5. Объем и основные растворители
        v_solution_ml_str = input_summary_data.get("V_solution_ml", "?")
        main_solvents_mix = input_summary_data.get(
            "main_solvents_mix_input", []
        )

        lines.append(f"V_solv = {v_solution_ml_str} [мл]")

        try:
            v_solution_ml_dec = Decimal(str(v_solution_ml_str))
            v_solv_line = f"V_solv = {v_solution_ml_dec.quantize(Decimal('0.01'))} [мл]"

            if len(main_solvents_mix) > 1 and v_solution_ml_dec > Decimal("0"):
                solvent_details_parts = []
                for solvent_item in main_solvents_mix:
                    symbol = solvent_item.get("symbol", "?")
                    fraction_str = solvent_item.get("fraction", "0")
                    try:
                        fraction_dec = Decimal(fraction_str)
                        individual_volume = (v_solution_ml_dec * fraction_dec).quantize(
                            Decimal("0.01")
                        )
                        if individual_volume > Decimal(
                            "1e-9"
                        ):  # Показываем только если объем значим
                            solvent_details_parts.append(
                                f"{symbol} = {individual_volume} [мл]"
                            )
                    except InvalidOperation:
                        solvent_details_parts.append(f"{symbol} = ? [мл]")
                if solvent_details_parts:
                    v_solv_line += f" ({', '.join(solvent_details_parts)})"
            lines.append(v_solv_line)
        except (InvalidOperation, TypeError):
            lines.append(f"V_solv = {v_solution_ml_str} [мл]")

        # 6. Антирастворитель и его объём
        antisolvents_mix: List[Dict[str, str]] = input_summary_data.get(
            "antisolvents_mix_input", []
        )
        v_antisolvent_ml_str = input_summary_data.get("V_antisolvent_ml_input", "0")

        try:
            v_antisolvent_ml_dec = Decimal(str(v_antisolvent_ml_str))
            if antisolvents_mix and v_antisolvent_ml_dec > Decimal("0"):
                antisolvent_names_parts = []
                antisolvent_volume_details_parts = []

                is_single_antisolvent_effective = False
                if len(antisolvents_mix) == 1:
                    try:
                        frac_dec = Decimal(antisolvents_mix[0].get("fraction", "1.0"))
                        if abs(frac_dec - Decimal("1.0")) < Decimal("0.001"):
                            is_single_antisolvent_effective = True
                            antisolvent_names_parts.append(
                                antisolvents_mix[0].get("symbol", "?")
                            )
                    except InvalidOperation:
                        pass  # Останется не single

                if (
                    not is_single_antisolvent_effective
                ):  # Если смесь или одна фракция не 1.0
                    for solvent_item in antisolvents_mix:
                        symbol = solvent_item.get("symbol", "?")
                        fraction_str = solvent_item.get("fraction", "0")
                        try:
                            fraction_dec = Decimal(fraction_str)
                            individual_volume = (
                                v_antisolvent_ml_dec * fraction_dec
                            ).quantize(Decimal("0.01"))
                            if individual_volume > Decimal("1e-9"):
                                antisolvent_volume_details_parts.append(
                                    f"{symbol} = {individual_volume} [мл]"
                                )
                                if (
                                    symbol not in antisolvent_names_parts
                                ):  # Для отображения в первой части
                                    antisolvent_names_parts.append(symbol)
                        except InvalidOperation:
                            antisolvent_volume_details_parts.append(
                                f"{symbol} = ? [мл]"
                            )
                            if symbol not in antisolvent_names_parts:
                                antisolvent_names_parts.append(symbol)

                antisolvents_display_name = (
                    "/".join(antisolvent_names_parts)
                    if antisolvent_names_parts
                    else "[Антирастворитель?]"
                )

                v_anti_line = f"{antisolvents_display_name}, V_anti = {v_antisolvent_ml_dec.quantize(Decimal('0.01'))} [мл]"
                if (
                    antisolvent_volume_details_parts
                    and not is_single_antisolvent_effective
                ):
                    v_anti_line += f" ({', '.join(antisolvent_volume_details_parts)})"
                lines.append(v_anti_line)
        except (InvalidOperation, TypeError):
            if (
                antisolvents_mix
                and v_antisolvent_ml_str != "0"
                and v_antisolvent_ml_str != ""
            ):
                lines.append(
                    f"[Антирастворитель?], V_anti = {v_antisolvent_ml_str} [мл]"
                )

        # 7. Коэффициенты избытка
        k_factors_settings: Dict[str, str] = input_summary_data.get(
            "individual_k_factors_settings", {}
        )
        k_factors_display_parts = []
        if k_factors_settings:  # Проверяем, что словарь не пуст
            sorted_k_salts = sorted(
                k_factors_settings.keys(), key=display_formatters.sort_key_salt
            )
            for salt_k in sorted_k_salts:
                k_value_str = k_factors_settings[salt_k]
                try:
                    k_value_dec = Decimal(k_value_str)
                    # Отображаем K только если он не равен 1.0 с некоторой точностью
                    if abs(k_value_dec - Decimal("1.0")) > Decimal("1e-9"):
                        k_factors_display_parts.append(
                            f"K({salt_k}) = {k_value_dec.quantize(Decimal('0.01'))}"
                        )
                except InvalidOperation:
                    k_factors_display_parts.append(
                        f"K({salt_k}) = {k_value_str} (ошибка)"
                    )
        if k_factors_display_parts:
            lines.append(", ".join(k_factors_display_parts))

        # 8. Массы каждой соли
        masses_g_data = equation_data.get("masses_g_final_k", {})
        masses_display_parts = []
        if masses_g_data:
            sorted_mass_salts = sorted(
                masses_g_data.keys(), key=display_formatters.sort_key_salt
            )
            for salt_m in sorted_mass_salts:
                mass_val = masses_g_data[salt_m]
                if mass_val is not None and mass_val != "MASS_ERROR":
                    try:
                        mass_dec = Decimal(str(mass_val))
                        # Используем 4 знака после запятой для масс, как в основной таблице
                        mass_str = f"{mass_dec.quantize(Decimal('0.0001'))}"
                        masses_display_parts.append(f"{salt_m} = {mass_str} [г]")
                    except (InvalidOperation, TypeError):
                        masses_display_parts.append(
                            f"{salt_m} = {mass_val} [г] (ошибка)"
                        )
                elif mass_val == "MASS_ERROR":
                    masses_display_parts.append(f"{salt_m} = ОшибкаММ [г]")

        if masses_display_parts:
            lines.append(", ".join(masses_display_parts))

        return "\n".join(lines)

    except Exception as e:
        logger.error(
            f"SUMMARY_SERVICE: Ошибка при формировании текста сводки: {e}",
            exc_info=True,
        )
        return f"Ошибка при формировании сводки:\n{str(e)}"