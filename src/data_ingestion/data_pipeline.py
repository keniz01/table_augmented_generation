import os
import sys
import pandas as pd
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database_models import DatabaseMetaData
from language_models import EmbeddingModel

# Database folder
def get_meta_data_schema_sql() -> str:
    with open(f'{SCRIPT_DIR}/sql/database_schema.sql') as file:
        return file.read()

def save_embeddings(get_meta_data_schema_sql):
    embed_model=EmbeddingModel()
    try:
        connection_string=os.environ.get('DATABASE_URL')
        engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'})

        with Session(engine, expire_on_commit=False) as session:
            
            with session.begin():
                rows=[]
                conn=engine.connect()
                df = pd.read_sql_query(con=conn, sql=get_meta_data_schema_sql())

                table_names=df["table_name"].unique()

                for table_name in table_names:
                    documents=df[df['table_name'] == table_name]
                    csv=documents.to_csv(index=False, header=False)

                    row=DatabaseMetaData(
                        table_name=table_name, 
                        table_description=df["table_description"][0],
                        table_meta_data=csv, 
                        vector_embeddings=embed_model.embed(csv)
                    )
                    rows.append(row)
                print(rows)
                save_many(session, rows)
    except (Exception, psycopg.DatabaseError) as error:
     print('ERROR: ',error)
     raise Exception(f"Failed to create vector embeddings: {error}") from error

def save_many(session, rows):
    session.add_all(rows)         
    session.commit()

save_embeddings(get_meta_data_schema_sql)