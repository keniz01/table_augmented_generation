import itertools
import os
import pandas as pd
import psycopg
from sqlalchemy import create_engine
from language_models import EmbeddingModel
from psycopg.rows import dict_row

class DatabaseContextRetriever:

    _embed_model=EmbeddingModel()

    @classmethod
    def from_question(cls, question:str):
        try:
            query_vector=cls._embed_model.embed(question)
            connection_string=os.environ.get('DATABASE_URL')
            # engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
            sql ="""SELECT table_name, table_meta_data , (vector_embeddings <#> '{query_vector}') as cosine_similarity
FROM database_meta_data
ORDER BY cosine_similarity DESC
LIMIT 5;"""
            # with engine.connect() as conn:
            with psycopg.connect(conninfo=connection_string, row_factory=dict_row) as conn:
                # df=pd.read_sql_query(con=conn, sql=sql.format(query_vector=query_vector))
                # columns=df.columns.to_list()
                # data=list(itertools.chain.from_iterable([[item.split('\n') for item in row.split('\n') if item] for row in df["table_meta_data"].to_list()]))
                # rows=[row.split(',') for row in list(itertools.chain.from_iterable(data))]
                # columns=["table_schema","table_name","table_description","column_name","column_data_type","is_column_nullable","column_description","column_constraint_type"]
                # df = pd.DataFrame(rows, columns=columns)
                # table_schema=df.to_markdown(tablefmt="grid", index=False)
                # return table_schema
                cursor = conn.cursor()
                cursor.execute('SET SESSION search_path=music')
                sql=sql.format(query_vector=query_vector)
                cursor.execute(sql)
                records = cursor.fetchall()  
                return records   
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise Exception(f"Failed to retrieve similar metadata: {error}") from error