import os
import textwrap
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama
import psycopg
from sqlalchemy import create_engine, select, text
import pandas as pd
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, declarative_base
from database_models import DatabaseMetaData
from language_models import EmbeddingModel

chat_model = Llama(
   model_path="../models/Phi-3-mini-128k-instruct.Q6_K.gguf",
   n_ctx=2048,
   verbose=False,
   n_gpu_layers=0,
   logits_all=True,
   chat_format="chatml",
   temperature=0    
)
 
user_query="Can you show all album titles by artist Capleton release on label Jet Star?"

embed_model=EmbeddingModel()
query_embeddings=embed_model.embed(user_query)

try:
    connection_string=os.environ.get('DATABASE_URL')
    engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'},echo=True)
    Session = sessionmaker(engine)

    with engine.connect() as conn:
        with Session(bind=conn) as session:
            select_statement=select(DatabaseMetaData).order_by(DatabaseMetaData.vector_embeddings.cosine_distance(query_embeddings)).limit(4)
            result=session.scalars(select_statement).all()
            most_similar_documents=[item for item in result]
            
except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise Exception(f"Failed to retrieve vector embeddings: {error}") from error

context = ""
for _, document in enumerate(most_similar_documents):
	wrapped_text=textwrap.fill(document.table_json_schema,width=100)
	context += wrapped_text

prompt_template=f"""
<|system|>
You are a PostgreSQL expert. Generate correct a correct SQL statement from the context information provided to answer the question at the end.
You must use only the column names provided in the context, don't make up column names. If you can't find an answer, say you dont know.
Do not wrap the response in any backticks (```) or anything else. Respond with a valid SQL statement only.
Do not return comments, assumptions or sequence of steps.
Adhere to these rules:
- Use ILIKE when comparing case sensitive strings instead of the equal (=) operator.
- Always use table and columns aliases.
- No INSERT, UPDATE, DELETE instructions, CREATE, ALTER or DROP instructions.
<|end|>
<|user|>
Context: 
{context}
Question: {user_query}<|end|>
<|assistant|>
"""

output=chat_model(prompt_template, max_tokens=2048, echo=True)
sql_query=output["choices"][0]["text"].strip()
print(sql_query)