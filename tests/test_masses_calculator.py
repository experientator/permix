# tests/test_masses_calculator.py

import pytest
from unittest.mock import patch
from src.utils.masses_calculator import calculate_precursor_masses

def test_calculate_masses_for_simple_mapbi3():
    template_id = 7
    anion_stoichiometry = 3

    cations = [
        {
            "structure_type": "a_site", "symbol": "MA", "fraction": "1.0",
            "valence": 1, "stoichiometry": 1.0, "real_stoichiometry": 1.0
        },
        {
            "structure_type": "b_site", "symbol": "Pb", "fraction": "1.0",
            "valence": 2, "stoichiometry": 1.0, "real_stoichiometry": 1.0
        }
    ]

    anions = [{"symbol": "I", "fraction": "1.0"}]

    solution_info = {
        "c_solvent": 1.0,
        "v_solvent": 1.0,
        "v_antisolvent": 0.0
    }

    solvents = [{"solvent_type": "solvent", "symbol": "DMF", "fraction": "1.0"}]
    k_factors = []

    results = calculate_precursor_masses(
        template_id, cations, anions, anion_stoichiometry,
        solution_info, solvents, k_factors
    )

    assert results is not None
    assert "equations" in results

    target_equation_data = None
    for eq_data in results["equations"].values():
        coeffs = eq_data.get("coefficients_detailed", {})
        if "MAI" in coeffs and "PbI2" in coeffs:
            target_equation_data = eq_data
            break

    assert target_equation_data is not None, "Equation using MAI and PbI2 was not found"

    masses = target_equation_data["masses_g_final_k"]

    # M(MAI) = 158.94 g/mol; M(PbI2) = 461.01 g/mol
    # For 1 mL of 1 M solution, we need 0.001 mol of product.
    expected_mai_mass = 0.001 * 158.94
    expected_pbi2_mass = 0.001 * 461.01

    assert masses.get("MAI") == pytest.approx(expected_mai_mass, abs=1e-4)
    assert masses.get("PbI2") == pytest.approx(expected_pbi2_mass, abs=1e-4)

def test_calculate_masses_with_k_factor():
    template_id = 7
    anion_stoichiometry = 3

    cations = [
        {"structure_type": "a_site", "symbol": "MA", "fraction": "1.0", "valence": 1, "stoichiometry": 1.0,
         "real_stoichiometry": 1.0},
        {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "valence": 2, "stoichiometry": 1.0,
         "real_stoichiometry": 1.0}
    ]
    anions = [{"symbol": "I", "fraction": "1.0"}]
    solution_info = {"c_solvent": 1.0, "v_solvent": 1.0, "v_antisolvent": 0.0}
    solvents = [{"solvent_type": "solvent", "symbol": "DMF", "fraction": "1.0"}]

    # Add a K-factor for MAI
    k_factors = [{"salt": "MAI", "k_factor": "1.1"}]

    # We need to mock database calls made by the mass calculator
    with patch('src.utils.masses_calculator.get_molar_mass_of_salt') as mock_get_mass:
        # Define the behavior of the mock
        def mass_logic(salt_formula):
            if salt_formula == "MAI":
                return 158.94
            if salt_formula == "PbI2":
                return 461.01
            return 0

        mock_get_mass.side_effect = mass_logic

        # ACT
        results = calculate_precursor_masses(
            template_id, cations, anions, anion_stoichiometry,
            solution_info, solvents, k_factors
        )

    # ASSERT
    assert results is not None
    target_equation_data = None
    for eq_data in results["equations"].values():
        if "MAI" in eq_data.get("coefficients_detailed", {}):
            target_equation_data = eq_data
            break

    assert target_equation_data is not None

    masses = target_equation_data["masses_g_final_k"]

    # Stoichiometric mass for MAI is 0.15894 g
    # With k-factor of 1.1, expected mass is 0.15894 * 1.1 = 0.174834 g
    expected_mai_mass_with_k = 0.15894 * 1.1
    expected_pbi2_mass = 0.46101  # PbI2 has no k-factor

    assert masses.get("MAI") == pytest.approx(expected_mai_mass_with_k, abs=1e-5)
    assert masses.get("PbI2") == pytest.approx(expected_pbi2_mass, abs=1e-5)