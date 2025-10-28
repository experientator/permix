# tests/test_database_utils.py

import pytest
from unittest.mock import patch, MagicMock
from src.utils.database_utils import (get_templates_list, get_template_id, get_candidate_cations,
                                      get_anion_stoichiometry, get_cation_formula, get_solvents, get_template_name)


@patch('src.utils.database_utils.sqlite3')
def test_get_templates_list(mock_sqlite3):
    # 1. ARRANGE: Configure the mock database connection and cursor
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    # Simulate the return value of fetchall()
    mock_cursor.fetchall.return_value = [
        ('3D ABX3',),
        ('2D A2BX4',),
        ('0D A4BX6',)
    ]

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    # 2. ACT: Call the function that uses the database
    templates = get_templates_list()

    # 3. ASSERT: Check the results and that the mock was used correctly
    assert templates == ['3D ABX3', '2D A2BX4', '0D A4BX6']
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT DISTINCT name FROM Phase_templates ORDER BY dimensionality")
    mock_connection.close.assert_called_once()


@patch('src.utils.database_utils.sqlite3')
def test_get_template_id(mock_sqlite3):
    # 1. ARRANGE
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    # Simulate the return value of fetchone()
    mock_cursor.fetchone.return_value = (7,)  # Return a tuple, as the real function does

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    template_name = "3D ABX3"

    # 2. ACT
    template_id = get_template_id(template_name)

    # 3. ASSERT
    assert template_id == 7
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT id FROM Phase_templates WHERE name = ?", (template_name,))
    mock_connection.close.assert_called_once()


@patch('src.utils.database_utils.sqlite3')
def test_get_candidate_cations(mock_sqlite3):
    # 1. ARRANGE
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    # Simulate the database returning a comma-separated string
    mock_cursor.fetchone.return_value = ('MA, FA, Cs',)

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    candidate_name = "a_site_val_1"

    # 2. ACT
    cations_list = get_candidate_cations(candidate_name)

    # 3. ASSERT
    # The function should parse the string into a list of stripped strings
    assert cations_list == ["MA", "FA", "Cs"]
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT cations FROM Candidate_cations WHERE name = ?",
                                                (candidate_name,))
    mock_connection.close.assert_called_once()


@patch('src.utils.database_utils.sqlite3')
def test_get_anion_stoichiometry(mock_sqlite3):
    # 1. ARRANGE
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_cursor.fetchone.return_value = (3,)  # Simulate fetching stoichiometry for ABX3

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    template_id = 7

    # 2. ACT
    stoichiometry = get_anion_stoichiometry(template_id)

    # 3. ASSERT
    assert stoichiometry == 3
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT anion_stoichiometry FROM Phase_templates WHERE id = ?",
                                                (template_id,))
    mock_connection.close.assert_called_once()


@patch('src.utils.database_utils.sqlite3')
def test_get_cation_formula(mock_sqlite3):
    # 1. ARRANGE
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    # Simulate fetching the formula for Formamidinium (FA)
    mock_cursor.fetchone.return_value = ('CH(NH2)2',)

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    cation_name = "FA"

    # 2. ACT
    formula = get_cation_formula(cation_name)

    # 3. ASSERT
    assert formula == 'CH(NH2)2'
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT formula FROM Ions WHERE name = ?", (cation_name,))
    mock_connection.close.assert_called_once()


@patch('src.utils.database_utils.sqlite3')
def test_get_solvents(mock_sqlite3):
    # 1. ARRANGE
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    # Simulate fetching a list of solvent names
    mock_cursor.fetchall.return_value = [('DMF',), ('DMSO',)]

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    solvent_type = "solvent"

    # 2. ACT
    solvents_list = get_solvents(solvent_type)

    # 3. ASSERT
    assert solvents_list == ["DMF", "DMSO"]
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT DISTINCT name FROM Solvents WHERE type = ?", (solvent_type,))
    mock_connection.close.assert_called_once()


@patch('src.utils.database_utils.sqlite3')
def test_get_template_name(mock_sqlite3):
    # 1. ARRANGE
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    mock_cursor.fetchone.return_value = ('3D ABX3',)

    mock_connection.cursor.return_value = mock_cursor
    mock_sqlite3.connect.return_value = mock_connection

    template_id = 7

    # 2. ACT
    template_name = get_template_name(template_id)

    # 3. ASSERT
    assert template_name == "3D ABX3"
    mock_sqlite3.connect.assert_called_once_with("data.db")
    mock_cursor.execute.assert_called_once_with("SELECT name FROM Phase_templates WHERE id = ?", (template_id,))
    mock_connection.close.assert_called_once()