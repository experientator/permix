# tests/language/test_manager.py

import pytest
from unittest.mock import MagicMock
# IMPORTANT: We import the instance that is actually used by the app
from src.language.manager import localization_manager


@pytest.fixture
def manager_with_mock_db(monkeypatch):
    # 1. Create a mock database object
    mock_db = MagicMock()

    # 2. Pre-program its behavior for different languages
    def get_translations_side_effect(language):
        if language == 'en':
            return {"greeting": "Hello"}
        if language == 'ru':
            return {"greeting": "Привет"}
        return {}

    mock_db.get_all_translations.side_effect = get_translations_side_effect

    # 3. Use monkeypatch to replace the REAL db object inside the manager instance
    monkeypatch.setattr(localization_manager, 'db', mock_db)

    # 4. Manually reset the manager to a known state (english)
    localization_manager.set_language('en')

    # 5. Return the already-patched manager instance
    return localization_manager

def test_initial_state_and_tr(manager_with_mock_db):
    # The fixture already sets the language to 'en'
    assert manager_with_mock_db.current_language == 'en'
    assert manager_with_mock_db.tr("greeting") == "Hello"

def test_tr_with_unknown_key(manager_with_mock_db):
    assert manager_with_mock_db.tr("unknown_key") == "unknown_key"

def test_set_language(manager_with_mock_db):
    # Act: Change the language
    manager_with_mock_db.set_language("ru")

    # Assert
    assert manager_with_mock_db.current_language == 'ru'
    assert manager_with_mock_db.tr("greeting") == "Привет"

    # Check that the mock db method was called
    manager_with_mock_db.db.get_all_translations.assert_called_with('ru')

def test_notify_observers(manager_with_mock_db):
    # Arrange an observer
    observer = MagicMock()
    observer.update_language = MagicMock()
    manager_with_mock_db.register_observer(observer)

    # Act: Change the language
    manager_with_mock_db.set_language("ru")

    # Assert
    observer.update_language.assert_called_once()

    # Clean up for other tests
    manager_with_mock_db.unregister_observer(observer)