import unittest
from unittest.mock import Mock
from src.agents.tools.table_schema_retriever import TableSchemaRetriever
from src.llm_models.embedding_model import EmbeddingModel
from src.database_utils import DatabaseUtils
import psycopg

class TestTableSchemaRetriever(unittest.TestCase):
    def setUp(self):
        self.mock_embedding_model = Mock(spec=EmbeddingModel)
        self.mock_db_utils = Mock(spec=DatabaseUtils)
        self.retriever = TableSchemaRetriever(self.mock_embedding_model, self.mock_db_utils)

    def test_from_question_success(self):
        # Arrange
        question = "What tables store user data?"
        fake_vector = '[0.1, 0.2, 0.3]'
        self.mock_embedding_model.embed_text.return_value = fake_vector

        fake_rows = [
            {'raw_json': {'table': 'users'}},
            {'raw_json': {'table': 'profiles'}},
        ]
        self.mock_db_utils.fetch_all_rows.return_value = fake_rows

        # Act
        result = self.retriever.from_question(question)

        # Assert
        self.mock_embedding_model.embed_text.assert_called_once_with(question)
        expected_sql = f"""SELECT raw_json, (embeddings <#> '{fake_vector}') as cosine_similarity
FROM vector_embeddings
ORDER BY cosine_similarity DESC
LIMIT 5;"""
        self.mock_db_utils.fetch_all_rows.assert_called_once_with(expected_sql)
        self.assertEqual(result, [{'table': 'users'}, {'table': 'profiles'}])

    def test_from_question_raises_exception(self):
        # Arrange
        self.mock_embedding_model.embed_text.side_effect = psycopg.DatabaseError("DB error")
        question = "Trigger error"

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.retriever.from_question(question)
        
        self.assertIn("Failed to get context", str(context.exception))
        self.mock_embedding_model.embed_text.assert_called_once_with(question)

if __name__ == '__main__':
    unittest.main()