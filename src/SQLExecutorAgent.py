from os import path
import os
from llama_cpp import Llama
import psycopg
from psycopg.rows import dict_row

model_path=path.abspath(path.join(__file__ ,"../../.."))

class SQLExecutorAgent():
    def __init__(self):
        self.model = Llama(
            model_path=f"{model_path}//models/Phi-3.5-mini-instruct-Q6_K_L.gguf",
            n_ctx=2500,
            verbose=False,
            temperature=0    
        )
           
    def execute_sql(self, sql_statement:str) -> str:
        try:
            connection_string=os.environ.get('DATABASE_URL')
            conn = psycopg.connect(conninfo=connection_string, row_factory=dict_row)
            cursor = conn.cursor()
            cursor.execute('SET SESSION search_path=music')
            cursor.execute(sql_statement)
            sql_response_context = cursor.fetchall() 
            return sql_response_context
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise error
