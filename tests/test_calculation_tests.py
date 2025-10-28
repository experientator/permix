# tests/test_calculation_tests.py

import pytest
from unittest.mock import patch
from src.utils.calculation_tests import float_test, fraction_test


# Patching the localization_manager to avoid dependency on language files
@patch('src.utils.calculation_tests.localization_manager')
def test_float_test_valid_input(mock_lm):
    mock_lm.tr.return_value = "some text"
    assert float_test("123.45", "test value") == 123.45
    assert float_test("-10", "test value") == -10.0
    assert float_test(50, "test value") == 50.0


@patch('src.utils.calculation_tests.show_error')
@patch('src.utils.calculation_tests.localization_manager')
def test_float_test_invalid_input_shows_error(mock_lm, mock_showerror):
    mock_lm.tr.return_value = "some error message"
    result = float_test("not a number", "test value")

    assert result is None

    mock_showerror.assert_called_once()
    # CORRECT WAY: Get keyword arguments, because show_error is called with message=...
    call_kwargs = mock_showerror.call_args.kwargs
    assert "message" in call_kwargs
    assert "test value" in call_kwargs["message"]


@patch('src.utils.calculation_tests.show_error')
@patch('src.utils.calculation_tests.localization_manager')
def test_fraction_test_valid_fractions(mock_lm, mock_showerror):
    mock_lm.tr.return_value = "some text"

    data = [{'fraction': '0.5'}, {'fraction': '0.5'}]
    fractions_dict = {'anions': 0.0}

    try:
        fraction_test(data, fractions_dict, 'anion')
    except ValueError:
        pytest.fail("fraction_test raised ValueError unexpectedly for valid fractions")

    assert fractions_dict['anions'] == pytest.approx(1.0)
    mock_showerror.assert_not_called()


@patch('src.utils.calculation_tests.show_error')
@patch('src.utils.calculation_tests.localization_manager')
def test_fraction_test_invalid_sum_raises_error(mock_lm, mock_showerror):
    mock_lm.tr.return_value = "some error message"

    data = [{'fraction': '0.5'}, {'fraction': '0.6'}]  # Sums to 1.1
    fractions_dict = {'anions': 0.0}

    with pytest.raises(ValueError):
        fraction_test(data, fractions_dict, 'anion')

    mock_showerror.assert_called_once()
    # CORRECT WAY: Get keyword arguments
    call_kwargs = mock_showerror.call_args.kwargs
    assert "message" in call_kwargs
    assert "anions" in call_kwargs["message"]