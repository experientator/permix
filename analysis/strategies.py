import tkinter.messagebox
from itertools import combinations

from analysis.chemistry_utils import get_salt_formula
from analysis.geometry_calculator import show_error
import analysis.constants as constants

ANION_REQ_ZERO_THRESHOLD = 1e-6
COEFF_ZERO_THRESH = 1e-6
ZERO_THRESHOLD = 1e-9
COEFF_QUANT_PREC = 0.00001

class StrategyCalculationError(ValueError):
    pass

def _calculate_coefficients_all_flexible(flexible_cations, anions):
    coeffs_all_flex = {}
    error_msg = None
    active_target_anions = {
        hal: moles
        for hal, moles in anions.items()
    }
    if not active_target_anions:
        return {}, None
    if not flexible_cations:
        return {}, None
    total_active_target_anion_moles = sum(active_target_anions.values())

    for cation_data in flexible_cations:
        cs, csip, cv = (
            cation_data["symbol"],
            float(cation_data["real_stoichiometry"]),
            int(cation_data["valence"]),
        )
        for hs, tmh in active_target_anions.items():
            anion_frac = tmh / total_active_target_anion_moles
            sc = csip * anion_frac
            try:
                sf = get_salt_formula(cs, hs, cv)
                coeffs_all_flex[sf] = coeffs_all_flex.get(sf, 0) + sc
            except ValueError as e:
                err_det = f"Ошибка соли {cs}(V)-{hs}: {e}"
                error_msg = (error_msg + "; " if error_msg else "") + err_det
                show_error(f"STRAT_CALC: _all_flex: {err_det}")
                return None, error_msg
    return (None, error_msg) if error_msg else (coeffs_all_flex, None)


def _calculate_coefficients_compensatory(rigid_cations, flexible_cations,
                                         base_X_anion_for_rigid,
                                         target_anion_moles_map):
    coeffs = {}
    error_msg = None
    anions_provided_by_rigid = {
        h: 0 for h in constants.halides
    }

    for rc_data in rigid_cations:
        rcs, rcsip, rcv = (
            rc_data["symbol"],
            float(rc_data["real_stoichiometry"]),
            int(rc_data["valence"]),
        )
        rc_sc = rcsip
        try:
            rc_sf = get_salt_formula(rcs, base_X_anion_for_rigid, rcv)
            coeffs[rc_sf] = round(coeffs.get(rc_sf, 0) + rc_sc, 3)
            if base_X_anion_for_rigid in anions_provided_by_rigid:
                anions_provided_by_rigid[base_X_anion_for_rigid] += rc_sc * rcv
        except ValueError as e:
            err_det = f"Ошибка соли жесткого {rcs}(F)-{base_X_anion_for_rigid}: {e}"
            error_msg = (error_msg + "; " if error_msg else "") + err_det
            show_error(f"STRAT_CALC: _compensatory: {err_det}")
            return None, error_msg

    required_anions_from_flex = {}
    possible = True
    for hs in constants.halides:
        target = float(target_anion_moles_map.get(hs, 0.0))
        provided = float(anions_provided_by_rigid.get(hs, 0.0))
        required = target - provided

        if required < -ANION_REQ_ZERO_THRESHOLD:
            possible = False
            break

        if abs(required) >= ANION_REQ_ZERO_THRESHOLD:
            required_anions_from_flex[hs] = max(0.0, required)
        else:
            required_anions_from_flex[hs] = 0.0

    if not possible:
        return {}, None

    if not flexible_cations:
        if any(
            abs(req) > ANION_REQ_ZERO_THRESHOLD
            for req in required_anions_from_flex.values()
        ):
            return {}, None
        return coeffs, None

    anions_actually_provided_by_flex = {
        h: 0 for h in constants.halides
    }

    # --- ИСПРАВЛЕННАЯ ЛОГИКА ДЛЯ ГИБКИХ КАТИОНОВ ---
    active_required_anions_list = [
        h for h, m in required_anions_from_flex.items()
    ]
    total_remaining_anion_need_from_flex = sum(required_anions_from_flex.values())

    for fc_data in flexible_cations:
        fcs, fcsip, fcv = (
            fc_data["symbol"],
            float(fc_data["real_stoichiometry"]),
            int(fc_data["valence"]),
        )
        # if total_remaining_anion_need_from_flex <= 1e-9:
        #     # Если анионы от гибких не нужны, но сами гибкие катионы нужны (fcsip > 0),
        #     # то эти катионы не могут войти в состав без анионов. Стратегия невалидна.
        #     print(
        #         f"STRAT_CALC: _compensatory: Гибкий катион {fcs} (стех. {fcsip}) нужен, но анионы от гибких не требуются. Невалидная стратегия."
        #     )
        #     return {}, None

        # Стратегия 1: Если требуется только ОДИН тип аниона от гибких
        if len(active_required_anions_list) == 1:
            chosen_anion = active_required_anions_list[0]
            # Коэффициент соли равен стехиометрии катиона в продукте
            fc_salt_coeff = fcsip
            try:
                fc_sf = get_salt_formula(fcs, chosen_anion, fcv)
                coeffs[fc_sf] = round(coeffs.get(fc_sf, 0) + fc_salt_coeff, 3)
                anions_actually_provided_by_flex[
                    chosen_anion
                ] += fc_salt_coeff * fcv
            except ValueError as e:
                err_det = f"Ошибка соли гибкого {fcs}(V)-{chosen_anion}: {e}"
                error_msg = (error_msg + "; " if error_msg else "") + err_det
                return None, error_msg

        # Стратегия 2: Если требуется НЕСКОЛЬКО типов анионов от гибких
        elif len(active_required_anions_list) > 1:
            # Катион fcs (fcsip моль) должен распределить себя между солями с разными требуемыми анионами.
            # Распределение происходит пропорционально доле каждого требуемого аниона в общей остаточной потребности.
            for req_anion, moles_req_anion in required_anions_from_flex.items():
                if moles_req_anion <= ZERO_THRESHOLD:
                    continue

                # Доля этого требуемого аниона в общей остаточной потребности
                anion_share_in_total_need = (
                    moles_req_anion / total_remaining_anion_need_from_flex
                )

                # Коэффициент соли (fcs + req_anion) будет fcsip * anion_share_in_total_need
                # Это обеспечит, что суммарно по всем таким солям мы получим fcsip молей катиона fcs.
                partial_salt_coeff = fcsip * anion_share_in_total_need
                try:
                    fc_sf_partial = get_salt_formula(
                        fcs, req_anion, fcv
                    )
                    coeffs[fc_sf_partial] = round(
                        coeffs.get(fc_sf_partial, 0) + partial_salt_coeff, 3
                    )
                    anions_actually_provided_by_flex[
                        req_anion
                    ] += partial_salt_coeff * fcv
                except ValueError as e:
                    err_det = f"Ошибка соли гибкого {fcs}(V)-{req_anion}: {e}"
                    error_msg = (error_msg + "; " if error_msg else "") + err_det
                    return None, error_msg
        else:  # len(active_required_anions_list) == 0
            # Это условие уже было обработано проверкой total_remaining_anion_need_from_flex <= 0
            pass

    for hs_check in constants.halides:
        needed_from_flex = required_anions_from_flex.get(hs_check, 0)
        provided_by_fc_total = anions_actually_provided_by_flex.get(
            hs_check, 0
        )
        if abs(needed_from_flex - provided_by_fc_total) > ANION_REQ_ZERO_THRESHOLD:
            tkinter.messagebox.showinfo(message=
                f"STRAT_CALC: _compensatory: Дисбаланс для аниона {hs_check} от гибких катионов. "
                f"Требовалось от гибких: {needed_from_flex:.4f}, предоставлено гибкими: {provided_by_fc_total:.4f}. Стратегия невалидна."
            )
            return {}, None

    return coeffs, error_msg.strip() if error_msg else None


def calculate_strategies_coefficients(active_cations_details,
                                      target_anion_moles_map,
                                      base_X_anion_for_rigid):
    results_by_strategy = {}
    n_active_cations = len(active_cations_details)
    num_combinations_processed = 0

    start_num_flexible = 1 if n_active_cations > 1 else 0

    for num_flexible_cations in range(start_num_flexible, n_active_cations + 1):
        for flex_indices_tuple in combinations(
            range(n_active_cations), num_flexible_cations
        ):
            num_combinations_processed += 1
            flex_indices = list(flex_indices_tuple)
            flexible_group = [active_cations_details[i] for i in flex_indices]
            rigid_group = [
                active_cations_details[i]
                for i in range(n_active_cations)
                if i not in flex_indices
            ]

            desc_flex_parts = [f"{c['symbol']}(V)" for c in flexible_group]
            desc_rigid_parts = [
                f"{c['symbol']}(F,{base_X_anion_for_rigid})" for c in rigid_group
            ]
            strategy_description_key = (
                ", ".join(sorted(desc_flex_parts + desc_rigid_parts))
                or "NoCationsStrategy"
            )

            current_coeffs = None
            current_error_msg = None

            if not rigid_group:
                if flexible_group:
                    current_coeffs, current_error_msg = (
                        _calculate_coefficients_all_flexible(
                            flexible_group, target_anion_moles_map
                        )
                    )
                else:
                    current_coeffs = {}
            else:
                current_coeffs, current_error_msg = (
                    _calculate_coefficients_compensatory(
                        rigid_group,
                        flexible_group,
                        base_X_anion_for_rigid,
                        target_anion_moles_map,
                    )
                )

            final_coeffs_for_strategy = {}
            if current_coeffs is not None:
                for salt, coeff_val in current_coeffs.items():
                    if abs(coeff_val) >= COEFF_ZERO_THRESH:
                        quantized_coeff = round((coeff_val / COEFF_QUANT_PREC) * COEFF_QUANT_PREC, 3)
                        if abs(quantized_coeff) > ZERO_THRESHOLD:
                            final_coeffs_for_strategy[salt] = quantized_coeff

            results_by_strategy[strategy_description_key] = {
                "coefficients": (
                    final_coeffs_for_strategy
                    if final_coeffs_for_strategy or not current_error_msg
                    else None
                ),
                "error_message": current_error_msg,
            }

    return results_by_strategy, num_combinations_processed
