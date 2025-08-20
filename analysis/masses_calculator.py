import logging
from decimal import ROUND_HALF_UP, Decimal
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from analysis.chemistry_utils import (calculate_target_product_moles,
                                      calculate_target_anion_moles,
                                      get_molar_mass_of_salt,
                                      determine_base_anion_for_rigid_cations)
from analysis.geometry_calculator import show_error
from analysis.strategies import calculate_strategies_coefficients

logger = logging.getLogger(__name__)

MASS_THRESHOLD_FOR_INCLUSION_MG = Decimal("1")
MASS_THRESHOLD_FOR_INCLUSION_G = MASS_THRESHOLD_FOR_INCLUSION_MG / Decimal("1000.0")


def calculate_precursor_masses(
    template_id,
    cations,
    anions,
    anion_stoichiometry,
    c_solution_molar,
    v_solution_ml,
    v_antisolvent_ml,
    solvents,
    antisolvents,
    individual_k_factors,
    target_currency):

    results = {"equations": {}, "error_message": None}

    n_target_product_moles = calculate_target_product_moles(
        c_solution_molar, v_solution_ml)

    target_anion_moles = (
        calculate_target_anion_moles(
            anions, anion_stoichiometry)
    )

    base_X_rigid = determine_base_anion_for_rigid_cations(
        target_anion_moles)

    calculated_strategies, num_combs_processed = (
        calculate_strategies_coefficients(
            cations, target_anion_moles, base_X_rigid)
    )

    equation_counter = 0
    for strategy_desc, strategy_data in calculated_strategies.items():
        strategy_coeffs = strategy_data.get("coefficients")
        strategy_error = strategy_data.get("error_message")

        if strategy_error:
            show_error(
                f"MASS_CALC_CORE: Стратегия '{strategy_desc}' пропущена: {strategy_error}"
            )
            continue

        current_eq_masses_final_k_filtered = {}

        total_mass_g_final_k_significant = 0.0

        num_significant_reagents_with_mass = 0

        has_mass_calculation_error_for_eq = False
        mass_error_details_for_eq = ""
        cost_issue_details_for_eq = ""

        for salt_formula, coeff_val in strategy_coeffs.items():
            molar_mass_salt = get_molar_mass_of_salt(salt_formula)
            mass_g_with_k = None

            mass_g_stoich = n_target_product_moles * coeff_val * molar_mass_salt
            k_for_this_salt = individual_k_factors.get(salt_formula, Decimal("1.0"))
            calculated_mass_g_with_k = mass_g_stoich * k_for_this_salt

            if calculated_mass_g_with_k < MASS_THRESHOLD_FOR_INCLUSION_G:
                current_eq_masses_final_k_filtered[salt_formula] = None
            else:
                mass_g_with_k = calculated_mass_g_with_k.quantize(
                    strategy_calculator.COEFF_QUANT_PREC, rounding=ROUND_HALF_UP
                )
                current_eq_masses_final_k_filtered[salt_formula] = mass_g_with_k
                total_mass_g_final_k_significant += mass_g_with_k
                num_significant_reagents_with_mass += 1

        if solvents and v_solution_ml > Decimal(0):
            for solvent_info in solvents:
                solvent_symbol = solvent_info["symbol"]
                solvent_fraction = solvent_info["fraction"]
                solvent_volume_ml = v_solution_ml * solvent_fraction

        if antisolvents and v_antisolvent_ml > Decimal(0):
            for antisolvent_info in antisolvents:
                antisolvent_symbol = antisolvent_info["symbol"]
                antisolvent_fraction = antisolvent_info["fraction"]
                antisolvent_volume_ml = v_antisolvent_ml * antisolvent_fraction

        equation_counter += 1
        eq_key = f"Equation {equation_counter}"

        eq_error_msg = ""
        if mass_error_details_for_eq:
            eq_error_msg += mass_error_details_for_eq
        if cost_issue_details_for_eq:
            eq_error_msg += cost_issue_details_for_eq

        results["equations"][eq_key] = {
            "eq_key_numeric": equation_counter,
            "description": strategy_desc,
            "condition_met": not has_mass_calculation_error_for_eq,
            "coefficients_detailed": strategy_coeffs,
            "masses_g_final_k": current_eq_masses_final_k_filtered,
            "total_mass_g_final_k": (
                total_mass_g_final_k_significant.quantize(
                    strategy_calculator.COEFF_QUANT_PREC, rounding=ROUND_HALF_UP
                )
                if not has_mass_calculation_error_for_eq
                and num_significant_reagents_with_mass > 0
                else (
                    app_config.MASS_ERROR_MARKER
                    if has_mass_calculation_error_for_eq
                    else Decimal(0)
                )
            ),
            "num_reagents": num_significant_reagents_with_mass,
            "error_message": eq_error_msg.strip().rstrip(";") if eq_error_msg else None,
        }

    if equation_counter == 0 and not results["error_message"]:
        if calculated_strategies:
            show_error(
                "Ни одна из сгенерированных стратегий не привела к валидному набору реагентов."
            )

    try:
        product_formula_str = display_formatters.generate_formula_string(
            cations, anions, template_data.get("sites", {})
        )
        results["product_formula_display"] = product_formula_str
    except Exception as e_formula:
        logger.error(
            f"MASS_CALC_CORE: Ошибка генерации строки формулы продукта: {e_formula}"
        )
        results["product_formula_display"] = "[Ошибка генерации формулы]"

    try:
        logger.info("MASS_CALC_CORE: Расчет геометрических факторов...")
        geometry_factors_res = geometry_calculator.calculate_geometry_factors(
            cation_config=cations,
            anion_config=anions,
            template_id=template_id,
        )
        results["geometry_factors"] = geometry_factors_res
        logger.info(
            f"MASS_CALC_CORE: Результаты расчета геом. факторов: {geometry_factors_res}"
        )
    except Exception as e_geom:
        logger.error(
            f"MASS_CALC_CORE: Ошибка при расчете геометрических факторов: {e_geom}",
            exc_info=True,
        )
        results["geometry_factors"] = {
            "error": f"Ошибка расчета геом. факторов: {type(e_geom).__name__}"
        }

    results["input_summary"] = {
        "template_id": template_id,
        "target_moles_product_total": n_target_product_moles.quantize(Decimal("1e-7")),
        "C_solution_molar": c_solution_molar.quantize(Decimal("1e-4")),
        "V_solution_ml": v_solution_ml.quantize(Decimal("1e-2")),
        "individual_k_factors_settings": {
            k: str(v.quantize(Decimal("1e-2"))) for k, v in individual_k_factors.items()
        },
        "anion_info_product_input": anions,
        "target_anion_moles_per_formula_unit": {
            k: str(v.quantize(Decimal("1e-6")))
            for k, v in target_anion_moles.items()
            if v > 0
        },
        "base_X_anion_for_rigid_cations": base_X_rigid,
        "num_active_cations_in_phase": len(cations),
        "num_strategies_generated": equation_counter,
        "num_combinations_processed": num_combs_processed,
        "main_solvents_mix_input": solvents,
        "antisolvents_mix_input": antisolvents,
        "V_antisolvent_ml_input": (
            v_antisolvent_ml
            if v_antisolvent_ml > 0.0
            else 0
        ),
        "_components_for_formula_gen": cations,
        "_anions_for_formula_gen": anions,
    }

    logger.info(
        f"MASS_CALC_CORE: Расчет завершен. Найдено валидных уравнений: {equation_counter}."
    )
    return results
