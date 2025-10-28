# tests/test_sort_equations.py

import pytest
from src.utils.sort_equations import sort_by_minimum_criteria, optimal_sort, get_criterion_value


# Mock localization manager as it's used to define criteria keys
@pytest.fixture(autouse=True)
def mock_localization(monkeypatch):
    mock_tr = {
        "ucv_crit_all": "Total mass",
        "ucv_crit_num": "Number of precursors",
        "ucv_crit_mass": "Mass of a specific precursor",
    }
    monkeypatch.setattr("src.utils.sort_equations.localization_manager.tr", mock_tr.get)


@pytest.fixture
def sample_equations():
    # A dictionary of sample equation data for sorting
    return {
        "Equation 1": {
            "eq_key_numeric": 1,
            "total_mass_g_final_k": 100.0,
            "num_reagents": 3,
            "masses_g_final_k": {"SaltA": 50.0, "SaltB": 50.0},
        },
        "Equation 2": {
            "eq_key_numeric": 2,
            "total_mass_g_final_k": 80.0,  # Lower is better
            "num_reagents": 2,  # Lower is better
            "masses_g_final_k": {"SaltA": 80.0},
        },
        "Equation 3": {
            "eq_key_numeric": 3,
            "total_mass_g_final_k": 120.0,
            "num_reagents": 2,
            "masses_g_final_k": {"SaltA": 60.0, "SaltC": 60.0},
        },
    }


def test_get_criterion_value(sample_equations):
    eq2 = sample_equations["Equation 2"]
    assert get_criterion_value(eq2, "Total mass") == 80.0
    assert get_criterion_value(eq2, "Number of precursors") == 2
    assert get_criterion_value(eq2, "Mass of a specific precursor", "SaltA") == 80.0
    assert get_criterion_value(eq2, "Mass of a specific precursor", "SaltB") is None


def test_sort_by_minimum_criteria_single_criterion(sample_equations):
    criteria = ["Total mass"]
    _, sorted_keys = sort_by_minimum_criteria(sample_equations, criteria, None)

    # Expected order by total mass: Eq2 (80), Eq1 (100), Eq3 (120)
    assert sorted_keys == ["Equation 2", "Equation 1", "Equation 3"]


def test_sort_by_minimum_criteria_multiple_criteria(sample_equations):
    # Sort by num_reagents (asc), then by total_mass (asc)
    criteria = ["Number of precursors", "Total mass"]
    _, sorted_keys = sort_by_minimum_criteria(sample_equations, criteria, None)

    # Group by num_reagents: {2: [Eq2, Eq3], 3: [Eq1]}
    # Sort within group 2 by total_mass: Eq2 (80) < Eq3 (120)
    # Final order: Eq2, Eq3, Eq1
    assert sorted_keys == ["Equation 2", "Equation 3", "Equation 1"]


def test_optimal_sort(sample_equations):
    # Optimal sort uses a weighted score. Lower is better, so higher score is better.
    # We will just check if it produces a sorted list of the correct length.
    # The exact order depends on the weights and normalization, which can be complex to assert.
    criteria = ["Total mass", "Number of precursors"]
    sorted_eqs, sorted_keys = optimal_sort(sample_equations, criteria, None)

    assert len(sorted_eqs) == 3
    assert len(sorted_keys) == 3

    # Check that scores were added and are decreasing (since reverse=True in sort)
    assert "score" in sorted_eqs[0]
    assert sorted_eqs[0]["score"] >= sorted_eqs[1]["score"]
    assert sorted_eqs[1]["score"] >= sorted_eqs[2]["score"]