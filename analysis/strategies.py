def _calculate_coefficients_all_flexible(flexible_cations, target_anion_moles_map)
    coeffs_all_flex= {}
    error_msg = None
    active_target_anions = {
        hal: moles
        for hal, moles in target_anion_moles_map.items()
        if moles > constants.ZERO_THRESHOLD and hal in constants.get_halides()
    }
    if not active_target_anions:
        return {}, None
    if not flexible_cations:
        return {}, None
    total_active_target_anion_moles = sum(active_target_anions.values())

    for cation_data in flexible_cations:
        cs, csip, cv = (
            cation_data["symbol"],
            cation_data["stoich_in_product_unit"],
            cation_data["valence"],
        )
        if cv == 0 or csip <= constants.ZERO_THRESHOLD:
            continue
        for hs, tmh in active_target_anions.items():
            anion_frac = tmh / total_active_target_anion_moles
            sc = csip * anion_frac
            if sc <= constants.ZERO_THRESHOLD:
                continue
            try:
                sf = chemistry_utils.get_salt_formula(cs, hs, cv)
                coeffs_all_flex[sf] = coeffs_all_flex.get(sf, Decimal(0)) + sc
            except ValueError as e:
                err_det = f"Ошибка соли {cs}(V)-{hs}: {e}"
                error_msg = (error_msg + "; " if error_msg else "") + err_det
                logger.warning(f"STRAT_CALC: _all_flex: {err_det}")
                return None, error_msg
    return (None, error_msg) if error_msg else (coeffs_all_flex, None)
