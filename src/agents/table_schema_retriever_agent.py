import psycopg
from database_utils import DatabaseUtils
from llm_models.text_embedding_model import TextEmbeddingModel

class TableSchemaRetrieverAgent:

    def __init__(self, text_embed_model: TextEmbeddingModel, db_utils: DatabaseUtils):
        self.__text_embed_model=text_embed_model
        self.__db_utils=db_utils
    
    def from_question(self, question:str):
        try:
            query_vector=self.__text_embed_model.embed_text(question)
            sql ="""SELECT raw_json, (embeddings <#> '{query_vector}') as cosine_similarity
FROM vector_embeddings
ORDER BY cosine_similarity DESC
LIMIT 5;"""
            sql=sql.format(query_vector=query_vector)
            rows=self.__db_utils.fetch_all_rows(sql)
            return [row['raw_json'] for row in rows]   
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise Exception(f"Failed to get context: {error}") from error