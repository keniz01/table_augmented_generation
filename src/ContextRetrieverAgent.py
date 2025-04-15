import os
import psycopg
from psycopg.rows import dict_row

from llm_models.EmbeddingModel import EmbeddingModel

class ContextRetrieverAgent:

    _embed_model=EmbeddingModel()

    @classmethod
    def from_question(cls, question:str):
        try:
            query_vector=cls._embed_model.embed(question)
            connection_string=os.environ.get('DATABASE_URL')
            sql ="""SELECT raw_json, (embeddings <#> '{query_vector}') as cosine_similarity
FROM vector_embeddings
ORDER BY cosine_similarity DESC
LIMIT 5;"""

            with psycopg.connect(conninfo=connection_string, row_factory=dict_row) as conn:
                cursor = conn.cursor()
                cursor.execute('SET SESSION search_path=music')
                sql=sql.format(query_vector=query_vector)
                cursor.execute(sql)
                rows = cursor.fetchall()  
                return [row['raw_json'] for row in rows]   
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise Exception(f"Failed to get context: {error}") from error