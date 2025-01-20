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

chat_model = Llama(
   model_path="../models/Phi-3-mini-128k-instruct.Q6_K.gguf",
   n_ctx=2048,
   verbose=False,
   n_gpu_layers=0,
   logits_all=True,
   chat_format="chatml",
   temperature=0    
)
 
embed_model=Llama(
  model_path='../models/bge-small-en-v1.5-q4_k_m.gguf',
  embedding=True,
  verbose=False,
  pooling_type=LLAMA_POOLING_TYPE_LAST
)

user_query="Can you show all albums by artist Capleton release on label Jet Star?"
query_embeddings=embed_model.embed(user_query, normalize=True)

# <-> Eucludian distance
# <=> Cosine Similarity ex. sikit learn cosine_similarity
# <#> Inner product ex. numpy dot
cosine_similarity_sql=text(f"SELECT table_json_schema, 1-(vector_embeddings <=> '{query_embeddings}') as cosine_similarity \
    FROM database_meta_data \
        ORDER BY cosine_similarity DESC \
            LIMIT 3;")
try:
    connection_string=os.environ.get('DATABASE_URL')
    engine = create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
    Session = sessionmaker(engine)

    with engine.connect() as conn:
        with Session(bind=conn) as session:
            metaDbTable=DatabaseMetaData()
            # select_stmt=select(metaDbTable.table_json_schema).order_by(metaDbTable.vector_embeddings.l2_distance(query_embeddings)).limit(3)
            result=session.execute(cosine_similarity_sql).fetchall()
            most_similar_documents=[item[0] for item in result]
            
except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise Exception(f"Failed to retrieve vector embeddings: {error}") from error

context = ""
for _, document in enumerate(most_similar_documents):
	wrapped_text=textwrap.fill(document,width=100)
	context += wrapped_text

print(context)

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

output=chat_model(prompt_template, max_tokens=2048)
sql_query=output["choices"][0]["text"].strip().replace('```sql', '').replace('```', '')
print(sql_query)