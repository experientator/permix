# tests/test_strategies.py

import pytest
from unittest.mock import patch
from src.utils.strategies import (_calculate_coefficients_compensatory, _calculate_coefficients_all_flexible,
                                  calculate_strategies_coefficients)

def test_compensatory_strategy_one_rigid_one_flexible():
    rigid_cations = [{
        "symbol": "Pb", "real_stoichiometry": 1.0, "valence": 2
    }]

    flexible_cations = [{
        "symbol": "MA", "real_stoichiometry": 1.0, "valence": 1
    }]

    base_X_anion_for_rigid = "I"

    target_anion_moles_map = {
        "F": 0.0,
        "Cl": 0.5,
        "Br": 0.5,
        "I": 2.0
    }

    coeffs, error_msg = _calculate_coefficients_compensatory(
        rigid_cations, flexible_cations, base_X_anion_for_rigid, target_anion_moles_map
    )

    assert error_msg is None
    assert coeffs is not None

    # Expected result:
    # Pb (rigid) needs 2 anions. It takes 2 'I' anions, forming 1 PbI2.
    # Anions provided by rigid: {"I": 2.0}.
    # Anions required from flexible: {"Cl": 0.5, "Br": 0.5, "I": 0.0}.
    # Total anion need from flex: 1.0 mole.
    # MA (flexible) provides 1 mole of anions.
    # It splits itself to provide the required Cl and Br.
    # 0.5 MACl and 0.5 MABr.

    expected_coeffs = {
        "PbI2": 1.0,
        "MACl": 0.5,
        "MABr": 0.5
    }

    assert coeffs.keys() == expected_coeffs.keys()
    for salt, coeff in expected_coeffs.items():
        assert coeffs[salt] == pytest.approx(coeff)

def test_all_flexible_strategy_two_cations():
    flexible_cations = [
        {"symbol": "MA", "real_stoichiometry": 0.5, "valence": 1},
        {"symbol": "FA", "real_stoichiometry": 0.5, "valence": 1}
    ]

    anions = {
        "Br": 1.5,
        "I": 1.5
    }

    coeffs, error_msg = _calculate_coefficients_all_flexible(flexible_cations, anions)

    assert error_msg is None
    assert coeffs is not None

    # Expected result:
    # Total anions = 1.5 (Br) + 1.5 (I) = 3.0.
    # Fraction of Br = 1.5 / 3.0 = 0.5.
    # Fraction of I = 1.5 / 3.0 = 0.5.
    #
    # For MA (0.5 mol):
    #   - Forms 0.5 * 0.5 = 0.25 mol of MABr
    #   - Forms 0.5 * 0.5 = 0.25 mol of MAI
    #
    # For FA (0.5 mol):
    #   - Forms 0.5 * 0.5 = 0.25 mol of FABr
    #   - Forms 0.5 * 0.5 = 0.25 mol of FAI

    expected_coeffs = {
        "MABr": 0.25,
        "MAI": 0.25,
        "FABr": 0.25,
        "FAI": 0.25
    }

    assert len(coeffs) == len(expected_coeffs)
    for salt, coeff in expected_coeffs.items():
        assert salt in coeffs
        assert coeffs[salt] == pytest.approx(coeff)

def test_compensatory_strategy_impossible_scenario():
    # Scenario: Rigid cation (Pb) requires 2 moles of 'I', but target only has 1.5 moles.

    rigid_cations = [{
        "symbol": "Pb", "real_stoichiometry": 1.0, "valence": 2
    }]

    flexible_cations = [{
        "symbol": "MA", "real_stoichiometry": 1.0, "valence": 1
    }]

    base_X_anion_for_rigid = "I"

    target_anion_moles_map = {
        "Br": 1.5,
        "I": 1.5  # Not enough 'I' for PbI2
    }

    coeffs, error_msg = _calculate_coefficients_compensatory(
        rigid_cations, flexible_cations, base_X_anion_for_rigid, target_anion_moles_map
    )

    # The function should recognize this strategy is impossible and return empty coefficients
    assert error_msg is None
    assert coeffs == {}

def test_compensatory_strategy_single_anion_type_from_flex():
    # Scenario: Rigid Pb takes all the 'I', leaving flex MA to provide only 'Br'.

    rigid_cations = [{
        "symbol": "Pb", "real_stoichiometry": 1.0, "valence": 2
    }]

    flexible_cations = [{
        "symbol": "MA", "real_stoichiometry": 1.0, "valence": 1
    }]

    base_X_anion_for_rigid = "I"

    # Target requires 2 'I' (which Pb will take) and 1 'Br' (which MA must provide).
    target_anion_moles_map = {
        "Br": 1.0,
        "I": 2.0
    }

    coeffs, error_msg = _calculate_coefficients_compensatory(
        rigid_cations, flexible_cations, base_X_anion_for_rigid, target_anion_moles_map
    )

    assert error_msg is None
    assert coeffs is not None

    # Expected:
    # 1. Pb (rigid) forms 1.0 PbI2, providing 2.0 moles of 'I'.
    # 2. Required from flex: {'Br': 1.0, 'I': 0.0}. Only one type of anion is needed.
    # 3. MA (flexible) must provide the 1.0 mole of 'Br', forming 1.0 MABr.

    expected_coeffs = {
        "PbI2": 1.0,
        "MABr": 1.0
    }

    assert coeffs == expected_coeffs


@patch('src.utils.strategies._calculate_coefficients_compensatory')
@patch('src.utils.strategies._calculate_coefficients_all_flexible')
def test_calculate_strategies_coefficients_generator(mock_all_flex, mock_compensatory):
    # ARRANGE
    active_cations = [
        {"symbol": "MA", "real_stoichiometry": 1.0, "valence": 1},
        {"symbol": "Pb", "real_stoichiometry": 1.0, "valence": 2}
    ]
    target_anion_moles = {"I": 3.0}
    base_X_rigid = "I"

    mock_all_flex.return_value = ({"all_flex_salt": 1.0}, None)
    mock_compensatory.return_value = ({"compensatory_salt": 1.0}, None)

    # ACT
    results, num_processed = calculate_strategies_coefficients(
        active_cations, target_anion_moles, base_X_rigid
    )

    # ASSERT
    # The code intentionally skips the "all rigid" case, so 2^n - 1 = 3 strategies.
    assert num_processed == 3
    assert len(results) == 3

    # Strategy 1: Both flexible -> calls _all_flexible
    assert "MA(V), Pb(V)" in results
    assert results["MA(V), Pb(V)"]["coefficients"] == {"all_flex_salt": 1.0}

    # Strategy 2 & 3: One rigid, one flexible -> calls _compensatory
    assert "MA(F,I), Pb(V)" in results
    assert "MA(V), Pb(F,I)" in results
    assert results["MA(V), Pb(F,I)"]["coefficients"] == {"compensatory_salt": 1.0}

    # Strategy 4 (All rigid) is NOT generated by the code
    assert "MA(F,I), Pb(F,I)" not in results

    assert mock_all_flex.call_count == 1
    assert mock_compensatory.call_count == 2