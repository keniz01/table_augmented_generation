import os
import textwrap
import psycopg
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from database_models import DatabaseMetaData
from language_models import EmbeddingModel

class DatabaseContextRetriever:

    _embed_model=EmbeddingModel()
    
    @classmethod
    def from_question(cls, question:str) -> str:
        try:
            query_embeddings=cls._embed_model.embed(question)
            connection_string=os.environ.get('DATABASE_URL')
            engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
            Session = sessionmaker(engine)

            with engine.connect() as conn:
                with Session(bind=conn) as session:
                    select_statement=select(DatabaseMetaData).order_by(DatabaseMetaData.vector_embeddings.cosine_distance(query_embeddings)).limit(4)
                    result=session.scalars(select_statement).all()
                    metadata=[item for item in result]
                    return cls.__get_question_metadata_context(metadata)
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise Exception(f"Failed to retrieve similar metadata: {error}") from error

    def __get_question_metadata_context(metadata: list[DatabaseMetaData]) ->str:
        context = ""
        for _, document in enumerate(metadata):
            wrapped_text=textwrap.fill(document.table_meta_data,width=100)
            context += wrapped_text
        return context