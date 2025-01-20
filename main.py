import json
import os
import textwrap
from llama_cpp import LLAMA_POOLING_TYPE_NONE, Llama
from datetime import date
import numpy as np
import psycopg
import pandas as pd
import sqlalchemy as db

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
  pooling_type=LLAMA_POOLING_TYPE_NONE
)

user_query="Which album contains the track 'pull up' and which artist released it?"
# user_query='List all tracks on the album Party Alliance Vol 3-Retail CD'
database_schema="""
{
    "table_schema": "music",
    "tables": [
        {
            "table_name": "album",
            "description": "The album table maintains the album data",
            "columns": [
                {
                    "column_name": "album_id",
                    "data_type": "integer",
                    "is_nullable": "NO",
                    "description": "The album_id column contains the primary key for the album table",
                    "constraint_type": "PRIMARY KEY"
                },
                {
                    "column_name": "artist_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The artist_id column maintains a reference to the artist.artist_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "duration",
                    "data_type": "character varying",
                    "is_nullable": "YES",
                    "description": "The duration column contains the time it takes an album to complete playing",
                    "constraint_type": null
                },
                {
                    "column_name": "genre_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The genre_id column maintains a reference to the genre.genre_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "label_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The label_id column maintains a reference to the record_label.label_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "release_year",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The release_year column contains the year the album was released",
                    "constraint_type": null
                },
                {
                    "column_name": "title",
                    "data_type": "character varying",
                    "is_nullable": "YES",
                    "description": "The title column contains the name of the album",
                    "constraint_type": null
                },
                {
                    "column_name": "total_tracks",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The total_tracks column contains number of tracks on the album",
                    "constraint_type": null
                }
            ]
        },
        {
            "table_name": "genre",
            "description": "The genre table maintains the genre data",
            "columns": [
                {
                    "column_name": "genre_id",
                    "data_type": "integer",
                    "is_nullable": "NO",
                    "description": "The genre_id column contains the primary key for the genre table",
                    "constraint_type": "PRIMARY KEY"
                },
                {
                    "column_name": "genre_name",
                    "data_type": "character varying",
                    "is_nullable": "NO",
                    "description": "The genre_name column contains the genre name",
                    "constraint_type": "UNIQUE"
                }
            ]
        },
        {
            "table_name": "record_label",
            "description": "The record_label table maintains the record label data",
            "coloumns": [
                {
                    "column_name": "label_id",
                    "data_type": "integer",
                    "is_nullable": "NO",
                    "description": "The label_id column contains the record_label table primary key",
                    "constraint_type": "PRIMARY KEY"
                },
                {
                    "column_name": "label_name",
                    "data_type": "character varying",
                    "is_nullable": "YES",
                    "description": "The label_name column contains the label name",
                    "constraint_type": "UNIQUE"
                }
            ]
        },
        {
            "table_name": "recording_artist",
            "description": "The recording_artist table maintains recording_artist data",
            "columns": [
                {
                    "column_name": "artist_id",
                    "data_type": "integer",
                    "is_nullable": "NO",
                    "description": "The artist_id column contains the recording_artist table primary key",
                    "constraint_type": "PRIMARY KEY"
                },
                {
                    "column_name": "artist_name",
                    "data_type": "character varying",
                    "is_nullable": "YES",
                    "description": "The artist_name columns contains recording artist name",
                    "constraint_type": "UNIQUE"
                }
            ]
        },
        {
            "table_name": "track",
            "description": "The track table maintains the track data",
            "columns": [
                {
                    "column_name": "album_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The album_id column maintains a reference to the album.album_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "artist_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The artist_id column maintains a reference to the artist.artist_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "duration",
                    "data_type": "character varying",
                    "is_nullable": "YES",
                    "description": "The duration column contains the time it takes a track to complete playing",
                    "constraint_type": null
                },
                {
                    "column_name": "genre_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The genre_id column maintains a reference to the genre.genre_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "label_id",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The label_id column maintains a reference to the record_label.label_id column",
                    "constraint_type": "FOREIGN KEY"
                },
                {
                    "column_name": "position",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The position column contains the position on the album the track is located",
                    "constraint_type": null
                },
                {
                    "column_name": "release_year",
                    "data_type": "integer",
                    "is_nullable": "YES",
                    "description": "The release_year column contains the year the track was released",
                    "constraint_type": null
                },
                {
                    "column_name": "title",
                    "data_type": "character varying",
                    "is_nullable": "YES",
                    "description": "The title column contains the name of the track",
                    "constraint_type": null
                },
                {
                    "column_name": "track_id",
                    "data_type": "integer",
                    "is_nullable": "NO",
                    "description": "The track_id column contains the primary key for the track table",
                    "constraint_type": "PRIMARY KEY"
                }
            ]
        }
    ]
}
"""

# documents=database_schema.split(";")
documents=json.loads(database_schema)["tables"]
query_embeddings=embed_model.embed(user_query)[1]
doc_embeddings=[]
for _, document in enumerate(documents):
	doc_embeddings.append(embed_model.embed(json.dumps(document))[1])

similarities=np.dot(doc_embeddings, query_embeddings)

top_3_idx=np.argsort(similarities, axis=0)[-3:][::1].tolist()
most_similar_documents=[documents[idx] for idx in top_3_idx]

context = ""
for _, document in enumerate(most_similar_documents):
	wrapped_text=textwrap.fill(json.dumps(document),width=100)
	context += wrapped_text
      
prompt_template=f"""
<|system|>
You are a PostgreSQL expert. Generate correct a correct SQL statement from the context information provided to answer the question at the end.
Use only the column names provided in the context, don't make up column names. If you can't find an answer, say you dont know.
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

connection_string=os.getenv('DATABASE_URL')

context=""
try:
    engine=db.create_engine('postgresql+psycopg://postgres:postgres@localhost:5432/analysis', connect_args={'options': '-csearch_path=music'})
    with engine.connect() as conn:
        df=pd.read_sql_query(sql=sql_query, con=conn)
        context=df.to_csv(index=False)
except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise error

if len(context) > 0:
	prompt_template=f"""<|system|>You are a summarizer chatbot. 
	Summarise the context information given into a meaningful response to answer the question.
	Do not return comments, assumptions or advice. If you dont know the answer,say "I dont know.".<|end|>
	<|user|>
	Context: 
	{context}
	Question: {user_query}<|end|>
	<|assistant|>"""
	print("CONTEXT: ", context)
	output=chat_model(prompt_template, temperature=0)
	response=output["choices"][0]["text"].strip()
	print(response)
else:
	print('I dont know')