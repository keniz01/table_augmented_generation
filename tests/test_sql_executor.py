import sys
import unittest
from unittest.mock import Mock
from src.agents.tools.sql_executor import SQLExecutor
from src.database_utils import DatabaseUtils
import psycopg

sys.path.append('.')

class TestSQLExecutor(unittest.TestCase):
    def setUp(self):
        self.mock_db_utils = Mock(spec=DatabaseUtils)
        self.executor = SQLExecutor(self.mock_db_utils)

    def test_execute_success(self):
        # Arrange
        expected_rows = [('row1',), ('row2',)]
        self.mock_db_utils.fetch_all_rows.return_value = expected_rows

        # Act
        result = self.executor.execute("SELECT * FROM test_table")

        # Assert
        self.mock_db_utils.fetch_all_rows.assert_called_once_with("SELECT * FROM test_table")
        self.assertEqual(result, expected_rows)

    def test_execute_raises_exception(self):
        # Arrange
        self.mock_db_utils.fetch_all_rows.side_effect = psycopg.DatabaseError("DB error")

        # Act & Assert
        with self.assertRaises(psycopg.DatabaseError):
            self.executor.execute("SELECT * FROM broken_table")

        self.mock_db_utils.fetch_all_rows.assert_called_once_with("SELECT * FROM broken_table")

if __name__ == '__main__':    
    unittest.main()