import json
import os
import sys
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database_models import VectorEmbeddings
from language_models import EmbeddingModel

# Database folder
def get_json_database_schema() -> list[str]:
    with open(f'{SCRIPT_DIR}/database_schema.json') as file:
        return json.loads(file.read())
    
def save_embeddings():
    embed_model=EmbeddingModel()
    try:
        connection_string=os.environ.get('DATABASE_URL')
        engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'})

        with Session(engine, expire_on_commit=False) as session:
            
            with session.begin():

                json_database_schema=get_json_database_schema()
                for json_database_schema_element in json_database_schema:
                    raw_json=json_database_schema_element
                    embeddings=embed_model.embed(json.dumps(json_database_schema_element))

                    row=VectorEmbeddings(
                        raw_json=raw_json,
                        embeddings=embeddings
                    )
                    session.add(row)
                session.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print('ERROR: ',error)
        raise Exception(f"Failed to create vector embeddings: {error}") from error

save_embeddings()