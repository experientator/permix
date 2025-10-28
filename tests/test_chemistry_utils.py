# tests/test_chemistry_utils.py

import pytest
from unittest.mock import patch
from src.utils.chemistry_utils import get_molar_mass_of_salt, get_salt_formula, generate_formula_string


@pytest.mark.parametrize("cation_name, cation_formula, halide, valence, expected_mass", [
    ("MA", "CH3NH3", "I", 1, 158.94),  # MAI
    ("Pb", "Pb", "I", 2, 461.01),  # PbI2
    ("FA", "CH(NH2)2", "Br", 1, 124.95),  # FABr
    ("Cs", "Cs", "Cl", 1, 168.36),  # CsCl
])

def test_get_molar_mass_of_salt(cation_name, cation_formula, halide, valence, expected_mass):
    salt_formula_str = get_salt_formula(cation_name, halide, valence)

    def mock_get_cation_formula(c_name):
        if c_name == cation_name:
            return cation_formula
        return None

    with patch('src.utils.chemistry_utils.get_cation_formula', side_effect=mock_get_cation_formula):
        molar_mass = get_molar_mass_of_salt(salt_formula_str)

    assert molar_mass == pytest.approx(expected_mass, abs=0.1)

def test_get_salt_formula():
    assert get_salt_formula("MA", "I", 1) == "MAI"
    assert get_salt_formula("Pb", "Cl", 2) == "PbCl2"
    assert get_salt_formula("In", "Br", "3") == "InBr3"  # Test with string valence


@pytest.mark.parametrize("cations_config, anions_config, anion_stoichiometry, expected_formula", [
    (
            [  # Simple MAPbI3
                {"structure_type": "a_site", "symbol": "MA", "fraction": "1.0", "stoichiometry": "1.0"},
                {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "stoichiometry": "1.0"},
            ],
            [{"symbol": "I", "fraction": "1.0"}],
            3,
            "MAPbI3"
    ),
    (
            [  # Mixed cation (MA0.5FA0.5)PbI3
                {"structure_type": "a_site", "symbol": "FA", "fraction": "0.5", "stoichiometry": "1.0"},
                {"structure_type": "a_site", "symbol": "MA", "fraction": "0.5", "stoichiometry": "1.0"},
                {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "stoichiometry": "1.0"},
            ],
            [{"symbol": "I", "fraction": "1.0"}],
            3,
            "(FA0.5MA0.5)PbI3"
    ),
    (
            [  # 2D structure (PEA)2PbI4
                {"structure_type": "spacer", "symbol": "PEA", "fraction": "1.0", "stoichiometry": "2.0"},
                {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "stoichiometry": "1.0"},
            ],
            [{"symbol": "I", "fraction": "1.0"}],
            4,
            "PEA2PbI4"
    ),
    (
            [  # Mixed halide CsPb(Br0.5I0.5)3
                {"structure_type": "a_site", "symbol": "Cs", "fraction": "1.0", "stoichiometry": "1.0"},
                {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "stoichiometry": "1.0"},
            ],
            [
                {"symbol": "I", "fraction": "0.5"},
                {"symbol": "Br", "fraction": "0.5"}
            ],
            3,
            "CsPb(I0.5Br0.5)3"
    )
])

def test_generate_formula_string(cations_config, anions_config, anion_stoichiometry, expected_formula):
    # The order of mixed components can vary, so we need a more flexible check

    # Sort components within each site for predictable output
    sorted_cations = sorted(cations_config, key=lambda x: (x['structure_type'], x['symbol']))
    sorted_anions = sorted(anions_config, key=lambda x: x['symbol'])

    formula = generate_formula_string(sorted_cations, sorted_anions, anion_stoichiometry)

    # This is a simplified check. For full robustness, one might parse the formula string.
    # For now, we'll check against a pre-sorted expected formula.
    # Note: The expected formulas have been adjusted to match the sorting.

    # Remapping expected formulas based on sorting
    if "FA0.5MA0.5" in expected_formula:
        expected_formula = "(FA0.5MA0.5)PbI3"  # FA comes before MA
    if "I0.5Br0.5" in expected_formula:
        expected_formula = "CsPb(Br0.5I0.5)3"  # Br comes before I

    assert formula == expected_formula