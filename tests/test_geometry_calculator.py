# tests/test_geometry_calculator.py

import pytest
from unittest.mock import patch, MagicMock
from src.utils.geometry_calculator import calculate_geometry_factors


@patch('src.utils.geometry_calculator.get_dimensionality')
@patch('src.utils.geometry_calculator.get_template_site_types')
@patch('src.utils.geometry_calculator.get_ionic_radius')
def test_geometry_factors_for_simple_mapbi3(mock_get_radius, mock_get_site_types, mock_get_dim):
    # 1. ARRANGE: Configure the mock functions

    # Mock database responses
    mock_get_dim.return_value = 3
    mock_get_site_types.return_value = (True, False, True, False)  # a_site, spacer, b_site, b_double

    def mock_radius_logic(name, charge, cn):
        radii_db_mock = {
            ("MA", 1, 12): 1.81,
            ("Pb", 2, 6): 1.19,
            ("I", 1, 6): 2.20,
        }
        return radii_db_mock.get((name, charge, cn))

    mock_get_radius.side_effect = mock_radius_logic

    # Input data for the function
    template_id = 7
    cation_config = [
        {"structure_type": "a_site", "symbol": "MA", "fraction": "1.0", "valence": 1},
        {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "valence": 2}
    ]
    anion_config = [
        {"symbol": "I", "fraction": "1.0", "valence": 1}
    ]

    # 2. ACT: Call the function under test
    results = calculate_geometry_factors(cation_config, anion_config, template_id)

    # 3. ASSERT: Check the results
    assert results is not None
    assert "error" not in results and results.get("error") is None

    # Check that database functions were called with correct parameters
    mock_get_dim.assert_called_once_with(template_id)
    mock_get_site_types.assert_called_once_with(template_id)

    # t = (1.81 + 2.20) / (sqrt(2) * (1.19 + 2.20)) ≈ 0.836
    # μ = 1.19 / 2.20 ≈ 0.541
    assert results.get("t") == pytest.approx(0.836, abs=1e-2)
    assert results.get("mu") == pytest.approx(0.541, abs=1e-2)

    assert results.get("mu_prime") is None
    assert results.get("mu_double_prime") is None


@patch('src.utils.geometry_calculator.get_dimensionality')
@patch('src.utils.geometry_calculator.get_template_site_types')
@patch('src.utils.geometry_calculator.get_ionic_radius')
def test_geometry_factors_for_double_perovskite(mock_get_radius, mock_get_site_types, mock_get_dim):
    # 1. ARRANGE: Configure mocks
    mock_get_dim.return_value = 3
    mock_get_site_types.return_value = (True, False, True, True)  # a_site, spacer, b_site, b_double

    def mock_radius_logic(name, charge, cn):
        radii_db_mock = {
            ("Cs", 1, 12): 1.88,
            ("Ag", 1, 6): 1.15,
            ("Bi", 3, 6): 0.76,
            ("Br", 1, 6): 1.96,
        }
        return radii_db_mock.get((name, charge, cn))

    mock_get_radius.side_effect = mock_radius_logic

    # Input data for Cs2AgBiBr6
    template_id = 1  # Assuming ID for a double perovskite template
    cation_config = [
        {"structure_type": "a_site", "symbol": "Cs", "fraction": "1.0", "valence": 1},
        {"structure_type": "b_site", "symbol": "Ag", "fraction": "1.0", "valence": 1},
        {"structure_type": "b_double", "symbol": "Bi", "fraction": "1.0", "valence": 3},
    ]
    anion_config = [
        {"symbol": "Br", "fraction": "1.0", "valence": 1}
    ]

    # 2. ACT: Call the function
    results = calculate_geometry_factors(cation_config, anion_config, template_id)

    # 3. ASSERT: Check results
    assert results is not None
    assert "error" not in results and results.get("error") is None

    # Expected values for Cs2AgBiBr6
    # rA=1.88, rB'=1.15, rB''=0.76, rX=1.96
    # rB_avg = (1.15 + 0.76) / 2 = 0.955
    # t = (1.88 + 1.96) / (sqrt(2) * (0.955 + 1.96)) ≈ 0.932
    # μ' = 1.15 / 1.96 ≈ 0.587
    # μ'' = 0.76 / 1.96 ≈ 0.388

    assert results.get("t") == pytest.approx(0.932, abs=1e-3)
    assert results.get("mu_prime") == pytest.approx(0.587, abs=1e-3)
    assert results.get("mu_double_prime") == pytest.approx(0.388, abs=1e-3)
    assert results.get("mu") is None


@patch('src.utils.geometry_calculator.get_dimensionality')
@patch('src.utils.geometry_calculator.get_template_site_types')
@patch('src.utils.geometry_calculator.get_ionic_radius')
@patch('src.utils.geometry_calculator.show_error')  # Also mock the error popup
def test_geometry_factors_with_missing_radius(mock_show_error, mock_get_radius, mock_get_site_types, mock_get_dim):
    # 1. ARRANGE: Configure mocks for a failure case
    mock_get_dim.return_value = 3
    mock_get_site_types.return_value = (True, False, True, False)

    def mock_radius_logic(name, charge, cn):
        # Simulate that Pb radius is missing
        if name == "Pb":
            return None

        radii_db_mock = {
            ("MA", 1, 12): 1.81,
            ("I", 1, 6): 2.20,
        }
        return radii_db_mock.get((name, charge, cn))

    mock_get_radius.side_effect = mock_radius_logic

    template_id = 7
    cation_config = [
        {"structure_type": "a_site", "symbol": "MA", "fraction": "1.0", "valence": 1},
        {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "valence": 2}
    ]
    anion_config = [
        {"symbol": "I", "fraction": "1.0", "valence": 1}
    ]

    # 2. ACT: Call the function
    results = calculate_geometry_factors(cation_config, anion_config, template_id)

    # 3. ASSERT: Check that the calculation failed gracefully
    assert results is not None

    # Both t and mu depend on rB, so they should be None
    assert results.get("t") is None
    assert results.get("mu") is None

    # Check that an error message was supposed to be shown to the user
    mock_show_error.assert_called()

    # Example of checking the error message content
    error_call_args = mock_show_error.call_args[0]  # Get positional arguments of the call
    assert "GEOM_CALC:" in error_call_args[0]
    assert "b_site" in error_call_args[0]


@patch('src.utils.geometry_calculator.get_dimensionality')
@patch('src.utils.geometry_calculator.get_template_site_types')
@patch('src.utils.geometry_calculator.get_ionic_radius')
def test_geometry_factors_for_2d_perovskite(mock_get_radius, mock_get_site_types, mock_get_dim):
    # 1. ARRANGE: Configure mocks for a 2D case
    mock_get_dim.return_value = 2  # Simulate a 2D structure
    mock_get_site_types.return_value = (False, True, True, False)  # spacer, no a_site, b_site, no b_double

    def mock_radius_logic(name, charge, cn):
        radii_db_mock = {
            ("PEA", 1, 12): 2.50,  # A large spacer cation
            ("Pb", 2, 6): 1.19,
            ("I", 1, 6): 2.20,
        }
        return radii_db_mock.get((name, charge, cn))

    mock_get_radius.side_effect = mock_radius_logic

    # Input data for a typical 2D perovskite like (PEA)2PbI4
    template_id = 4  # Assuming an ID for a 2D template
    cation_config = [
        {"structure_type": "spacer", "symbol": "PEA", "fraction": "1.0", "valence": 1},
        {"structure_type": "b_site", "symbol": "Pb", "fraction": "1.0", "valence": 2}
    ]
    anion_config = [
        {"symbol": "I", "fraction": "1.0", "valence": 1}
    ]

    # 2. ACT: Call the function
    results = calculate_geometry_factors(cation_config, anion_config, template_id)

    # 3. ASSERT: Check results
    assert results is not None
    assert "error" not in results and results.get("error") is None

    # For 2D, Goldschmidt tolerance factor is not applicable
    assert results.get("t") == "N/A"

    # Octahedral factor should still be calculated
    # μ = 1.19 / 2.20 ≈ 0.541
    assert results.get("mu") == pytest.approx(0.541, abs=1e-3)

    assert results.get("mu_prime") is None
    assert results.get("mu_double_prime") is None