# tests/language/test_database.py

import pytest
import sqlite3
from unittest.mock import patch
from src.language.database import LocalizationDB


@pytest.fixture
def db_and_mock_conn():
    # 1. Create a single, persistent in-memory database connection
    in_memory_conn = sqlite3.connect(":memory:")

    # 2. Manually create the table schema in our in-memory DB
    cursor = in_memory_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS localization (
            name TEXT PRIMARY KEY,
            en TEXT NOT NULL,
            ru TEXT NOT NULL
        )
    ''')
    in_memory_conn.commit()

    # 3. Create an instance of the class. We'll ignore its internal db_path.
    db = LocalizationDB()

    # 4. Patch 'sqlite3.connect' within the target module
    with patch('src.language.database.sqlite3.connect') as mock_connect:
        # 5. Make the patch always return our single in-memory connection
        mock_connect.return_value = in_memory_conn

        # 6. Yield the db instance to the test
        yield db

    # 7. Clean up after the test
    in_memory_conn.close()

def test_add_and_get_translation(db_and_mock_conn):
    db = db_and_mock_conn
    db.add_translation("greeting", "Hello", "Привет")

    assert db.get_translation("en", "greeting") == "Hello"
    assert db.get_translation("ru", "greeting") == "Привет"

def test_get_non_existent_translation(db_and_mock_conn):
    db = db_and_mock_conn
    assert db.get_translation("en", "farewell") == "farewell"

def test_get_all_translations(db_and_mock_conn):
    db = db_and_mock_conn
    translations_batch = [
        ("greeting", "Hello", "Привет"),
        ("farewell", "Goodbye", "Пока")
    ]
    db.add_batch_translations(translations_batch)

    all_en = db.get_all_translations("en")
    all_ru = db.get_all_translations("ru")

    expected_en = {"greeting": "Hello", "farewell": "Goodbye"}
    expected_ru = {"greeting": "Привет", "farewell": "Пока"}

    assert all_en == expected_en
    assert all_ru == expected_ru

def test_add_or_replace_translation(db_and_mock_conn):
    db = db_and_mock_conn
    db.add_translation("status", "Old", "Старый")
    db.add_translation("status", "New", "Новый")

    assert db.get_translation("en", "status") == "New"
    assert db.get_translation("ru", "status") == "Новый"