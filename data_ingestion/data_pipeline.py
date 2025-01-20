import os
import sys
sys.path.append(os.getcwd())
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama
import pandas as pd
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json
from database_models import DatabaseMetaData
from language_models import EmbeddingModel

# Database folder
def get_meta_data_schema_sql() -> str:
    with open('database_schema_json.sql') as file:
        return file.read()

def save_embeddings(get_meta_data_schema_sql):
    embed_model=EmbeddingModel().embed_model
    try:
        connection_string=os.environ.get('DATABASE_URL')
        engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'})

        with Session(engine, expire_on_commit=False) as session:
            
            with session.begin():
                rows=[]
                conn=engine.connect()
                df = pd.read_sql_query(con=conn, sql=get_meta_data_schema_sql())
                documents=df['table_schema_json'].to_list()
                embed_model=embed_model
                
                for document in documents:
                    row=DatabaseMetaData(
                        table_name=document["table_name"], 
                        table_description=document["table_description"],
                        table_json_schema=json.dumps(document), 
                        vector_embeddings=embed_model.embed(json.dumps(document), normalize=True)
                    )
                    rows.append(row)   

                save_many(session, rows)
    except (Exception, psycopg.DatabaseError) as error:
     print('ERROR: ',error)
     raise Exception(f"Failed to create vector embeddings: {error}") from error

def save_many(session, rows):
    session.add_all(rows)         
    session.commit()

save_embeddings(get_meta_data_schema_sql)