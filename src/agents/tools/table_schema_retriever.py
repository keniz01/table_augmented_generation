from typing import Dict, List
import psycopg
from database_utils import DatabaseUtils
from llm_models.embedding_model import EmbeddingModel

class TableSchemaRetriever:

    def __init__(self, embeding_model: EmbeddingModel, db_utils: DatabaseUtils):
        self.__embeding_model=embeding_model
        self.__db_utils=db_utils
    
    def from_question(self, question: str) -> List[Dict]:
        try:
            query_vector=self.__embeding_model.embed_text(question)
            sql ="""SELECT raw_json, (embeddings <#> '{query_vector}') as cosine_similarity
FROM vector_embeddings
ORDER BY cosine_similarity DESC
LIMIT 5;"""
            sql=sql.format(query_vector=query_vector)
            rows=self.__db_utils.fetch_all_rows(sql)
            result=[row['raw_json'] for row in rows]   
            return result
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise Exception(f"Failed to get context: {error}") from error