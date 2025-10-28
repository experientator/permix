# tests/conftest.py

import pytest
import sqlite3
import shutil
from pathlib import Path


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(tmpdir_factory):
    """
    This fixture runs once per test session.
    It copies the main database to a temporary location
    and makes the test functions run from a directory
    that contains this temporary database.
    """
    # Path to the original database in the project root
    root_dir = Path(__file__).parent.parent
    original_db_path = root_dir / "data.db"

    # Create a temporary directory for the test session
    temp_dir = tmpdir_factory.mktemp("data")
    temp_db_path = temp_dir / "data.db"

    # Copy the original database to the temporary directory
    if original_db_path.exists():
        shutil.copy(original_db_path, temp_db_path)
    else:
        # If the original DB doesn't exist, create an empty one for the tests
        # This prevents tests from failing if the main DB is missing.
        # You might need to add schema creation here if necessary.
        conn = sqlite3.connect(temp_db_path)
        conn.close()

    # This is the key part: 'monkeypatch' is a pytest fixture
    # that allows safely modifying environment for tests.
    # We change the current working directory for the duration of the test.
    # This makes all relative path lookups (like for 'data.db') work correctly.
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.chdir(temp_dir)

    # Yield control to the test session
    yield

    # Teardown code (runs after all tests are finished)
    monkeypatch.undo()