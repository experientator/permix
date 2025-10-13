from analysis.chemistry_utils import (calculate_target_product_moles,
                                      calculate_target_anion_moles,
                                      get_molar_mass_of_salt,
                                      determine_base_anion_for_rigid_cations,
                                      generate_formula_string)
from analysis.geometry_calculator import calculate_geometry_factors
from analysis.strategies import calculate_strategies_coefficients
from analysis.calculation_tests import float_test, show_error
from gui.language.manager import localization_manager

def calculate_precursor_masses(
    template_id, cations,
    anions, anion_stoichiometry,
    solution_info, solvents,
    k_factors):

    results = {"equations": {}, "error_message": None}

    n_target_product_moles = float(calculate_target_product_moles(
        solution_info["c_solvent"], solution_info["v_solvent"]))

    anion_moles = (
        calculate_target_anion_moles(
            anions, anion_stoichiometry))

    base_X_rigid = determine_base_anion_for_rigid_cations(anion_moles)

    calculated_strategies, num_combs_processed = (
        calculate_strategies_coefficients(
            cations, anion_moles, base_X_rigid))

    v_antisolvent = 0.0
    solvents_by_type = {solvent_type: [] for solvent_type in ["solvent", "antisolvent"]}

    equation_counter = 0
    unique_strategies = {}

    for solvent in solvents:
        solvent_type = solvent["solvent_type"]
        if solvent_type in solvents_by_type:
            solvents_by_type[solvent_type].append(solvent)

        for solv in solvents_by_type["solvent"]:
            float_test(solv["fraction"],
                       localization_manager.tr("amc1"))
            solvent_volume_ml = solution_info["v_solvent"] * float(solv["fraction"])

    if solvents_by_type["antisolvent"]:
        v_antisolvent = solution_info["v_antisolvent"]
        for antisolv in solvents_by_type["antisolvent"]:
            float_test(antisolv["fraction"],
                       localization_manager.tr("amc2"))
            antisolvent_volume_ml = solution_info["v_solvent"] * float(antisolv["fraction"])

    for strategy_desc, strategy_data in calculated_strategies.items():
        strategy_coeffs = strategy_data.get("coefficients")
        strategy_error = strategy_data.get("error_message")

        if strategy_error:
            er1 = localization_manager.tr("amc3")
            er2 = localization_manager.tr("amc4")
            show_error(
                f"MASS_CALC_CORE: {er1} '{strategy_desc}' {er2}: {strategy_error}"
            )
            continue

        if strategy_coeffs:
            coeffs_tuple = tuple(sorted(strategy_coeffs.items()))
            strategy_key = f"strategy_{hash(coeffs_tuple)}"

            if strategy_key in unique_strategies:
                continue
            unique_strategies[strategy_key] = True

        current_eq_masses_final_k_filtered = {}

        total_mass_g_final_k_significant = 0.0

        num_significant_reagents_with_mass = 0

        has_mass_calculation_error_for_eq = False

        k_for_this_salt = 0.0

        for salt_formula, coeff_val in strategy_coeffs.items():
            molar_mass_salt = float(get_molar_mass_of_salt(salt_formula))
            calculated_mass_g_with_k = None

            mass_g_stoich = n_target_product_moles * float(coeff_val) * molar_mass_salt
            for k_factor_salt in k_factors:
                if k_factor_salt["salt"] == salt_formula:
                    k_for_this_salt = float(k_factor_salt["k_factor"])
            if k_for_this_salt:
                calculated_mass_g_with_k = mass_g_stoich * k_for_this_salt
            else:
                calculated_mass_g_with_k = mass_g_stoich

            current_eq_masses_final_k_filtered[salt_formula] = calculated_mass_g_with_k
            total_mass_g_final_k_significant += calculated_mass_g_with_k
            num_significant_reagents_with_mass += 1

        equation_counter += 1
        eq_key = f"Equation {equation_counter}"

        results["equations"][eq_key] = {
            "eq_key_numeric": equation_counter,
            "description": strategy_desc,
            "condition_met": not has_mass_calculation_error_for_eq,
            "coefficients_detailed": strategy_coeffs,
            "masses_g_final_k": current_eq_masses_final_k_filtered,
            "total_mass_g_final_k": total_mass_g_final_k_significant,
            "num_reagents": num_significant_reagents_with_mass
        }

    if equation_counter == 0 and not results["error_message"]:
        if calculated_strategies:
            show_error(
                localization_manager.tr("amc5")
            )

    try:
        product_formula_str = generate_formula_string(
            cations, anions, anion_stoichiometry
        )
        results["product_formula_display"] = product_formula_str
    except Exception as e_formula:
        er = localization_manager.tr("amc6")
        show_error(
            f"MASS_CALC_CORE: {er}: {e_formula}"
        )
        results["product_formula_display"] = localization_manager.tr("amc7")
    #
    try:
        geometry_factors_res = calculate_geometry_factors(
            cation_config=cations,
            anion_config=anions,
            template_id=template_id,
        )
        results["geometry_factors"] = geometry_factors_res

    except Exception as e_geom:
        er = localization_manager.tr("amc8")
        show_error(
            f"MASS_CALC_CORE: {er}: {e_geom}"
        )
        results["geometry_factors"] = {
            "error": f"{er}: {type(e_geom).__name__}"
        }

    results["input_summary"] = {
        "template_id": template_id,
        "target_moles_product_total": n_target_product_moles,
        "C_solution_molar": solution_info["c_solvent"],
        "V_solution_ml": solution_info["v_solvent"],
        "individual_k_factors_settings": k_factors,
        "anion_info_product_input": anions,
        "target_anion_moles_per_formula_unit": anion_moles,
        "base_X_anion_for_rigid_cations": base_X_rigid,
        "num_active_cations_in_phase": len(cations),
        "num_strategies_generated": equation_counter,
        "num_combinations_processed": num_combs_processed,
        "main_solvents_mix_input": solvents_by_type["solvent"],
        "antisolvents_mix_input": solvents_by_type["antisolvent"],
        "V_antisolvent_ml_input": v_antisolvent,
        "_components_for_formula_gen": cations,
        "_anions_for_formula_gen": anions,
    }

    return results