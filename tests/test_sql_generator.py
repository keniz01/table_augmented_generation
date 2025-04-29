import unittest
from unittest.mock import Mock, patch
from src.agents.tools.sql_generator import SQLGenerator
from src.llm_models.instruction_model import InstructionModel

class TestSQLGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_llm_model = Mock(spec=InstructionModel)
        self.generator = SQLGenerator(self.mock_llm_model)

    @patch('src.agents.tools.sql_generator.SQLFormatHelper')
    def test_generate_sql_success(self, mock_sql_formatter_class):
        # Arrange
        mock_response = "SELECT * FROM users"
        formatted_sql = "SELECT * FROM users;"  # assuming format_sql adds a semicolon

        # Mock the behavior of get_response
        self.mock_llm_model.get_response.return_value = mock_response

        # Mock SQLFormatHelper behavior
        mock_formatter_instance = Mock()
        mock_formatter_instance.format_sql.return_value = formatted_sql
        mock_sql_formatter_class.return_value = mock_formatter_instance

        # Act
        result = self.generator.generate_sql("Get all users")

        # Assert
        self.mock_llm_model.get_response.assert_called_once_with("Get all users")
        mock_sql_formatter_class.assert_called_once_with(mock_response)
        mock_formatter_instance.format_sql.assert_called_once()
        self.assertEqual(result, formatted_sql)

    @patch('src.agents.tools.sql_generator.SQLFormatHelper')
    def test_generate_sql_handles_empty_response(self, mock_sql_formatter_class):
        # Arrange
        self.mock_llm_model.get_response.return_value = ""
        mock_formatter_instance = Mock()
        mock_formatter_instance.format_sql.return_value = ""
        mock_sql_formatter_class.return_value = mock_formatter_instance

        # Act
        result = self.generator.generate_sql("Get something")

        # Assert
        self.assertEqual(result, "")
        self.mock_llm_model.get_response.assert_called_once_with("Get something")
        mock_sql_formatter_class.assert_called_once_with("")
        mock_formatter_instance.format_sql.assert_called_once()

if __name__ == '__main__':
    unittest.main()