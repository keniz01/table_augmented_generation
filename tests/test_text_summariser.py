import unittest
from unittest.mock import MagicMock
from src.llm_models.instruction_model import InstructionModel
from src.agents.tools.text_summariser import TextSummariser

class TestTextSummariser(unittest.TestCase):

    def setUp(self):
        self.mock_llm = MagicMock(spec=InstructionModel)
        self.summariser = TextSummariser(self.mock_llm)

    def test_summarise_text_returns_expected_output(self):
        prompt = "Summarise the following article about AI advancements..."
        expected_summary = "AI has made significant progress in recent years."

        # Set up the mock response
        self.mock_llm.get_response.return_value = expected_summary

        # Call the method
        result = self.summariser.summarise_text(prompt)

        # Assertions
        self.mock_llm.get_response.assert_called_once_with(prompt)
        self.assertEqual(result, expected_summary)

    def test_summarise_text_with_empty_prompt(self):
        prompt = ""
        expected_summary = ""

        self.mock_llm.get_response.return_value = expected_summary
        result = self.summariser.summarise_text(prompt)

        self.mock_llm.get_response.assert_called_once_with(prompt)
        self.assertEqual(result, expected_summary)

if __name__ == "__main__":
    unittest.main()
