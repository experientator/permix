import periodictable

def calculate_formula_molar_mass(formula_str):

    try:
        parsed_entity = periodictable.formula(formula_str)
        molar_mass_float = float(parsed_entity.mass)
        molar_mass_dec = Decimal(str(molar_mass_float))
        return molar_mass_dec.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    except ValueError as ve:
        return None


def get_molar_mass_of_salt(salt_formula_str: str) -> Optional[Decimal]:
    """
    Рассчитывает молярную массу для простой соли прекурсора вида КлючКатионаГалогенИндекс.
    Если формат не распознан, пытается рассчитать как общую формулу, используя
    брутто-формулу катиона из constants.get_cation_formula_map().
    """
    cation_formulas_map = constants.get_cation_formula_map()
    # Регулярное выражение для разбора формулы соли: (КлючКатиона)(Галоген)(Индекс, если есть)
    match = re.match(r"([A-Z][a-zA-Z0-9_]*)(Cl|Br|I)(\d*)$", salt_formula_str.strip())

    if match:
        cation_key = match.group(1)
        halide_symbol = match.group(2)
        halide_index_str = match.group(3)
        halide_count = int(halide_index_str) if halide_index_str else 1

        # Получаем брутто-формулу катиона из карты.
        # Если ключ катиона не найден в карте, используем сам ключ как формулу (например, для "Pb", "Sn").
        actual_cation_formula_for_mass = cation_formulas_map.get(cation_key, cation_key)

        cation_mass = calculate_formula_molar_mass(actual_cation_formula_for_mass)
        halide_mass = calculate_formula_molar_mass(halide_symbol)
        total_mass = cation_mass + (Decimal(str(halide_count)) * halide_mass)
        logger.debug(
            f"  CHEM_UTILS: Рассчитана масса для соли '{salt_formula_str}' (через разбор): {total_mass:.4f}"
        )
        return total_mass.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    else:
        # Если не удалось разобрать как CationKey-Halide[Index],
        # пытаемся рассчитать как общую формулу.
        # Это может сработать, если salt_formula_str - это, например, "CH3NH3PbI3".
        logger.debug(
            f"  CHEM_UTILS: Формат '{salt_formula_str}' не распознан как CationKey-Halide[Index]. "
            "Выполняется общий расчет массы."
        )
        return calculate_formula_molar_mass(salt_formula_str)


def get_salt_formula(cation_key: str, halide: str, valence: int):
    return f"{cation_key}{halide}" if valence == 1 else f"{cation_key}{halide}{valence}"
