import os
import sys
from time import localtime, strftime
import pandas as pd
import psycopg
import sqlalchemy as db
import itertools

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.language_models import EmbeddingModel, InstructionModel
from src.sql_prompt import SqlPrompt

table_schema_query="""SELECT 
    tbl.table_schema, 
    tbl.table_name, 
    pgd_tbl.description table_description, 
    cols.column_name, 
    cols.data_type column_data_type, 
    cols.is_nullable is_column_nullable, 
    pgd_col.description column_description, 
    tc.constraint_type column_constraint_type
FROM information_schema.tables tbl
JOIN information_schema.columns cols ON cols.table_name = tbl.table_name
LEFT join information_schema.key_column_usage kcu on kcu.table_name = cols.table_name and kcu.column_name = cols.column_name
LEFT join information_schema.table_constraints tc on tc.table_name = cols.table_name and tc.constraint_name = kcu.constraint_name
JOIN pg_catalog.pg_namespace pgn ON pgn.nspname=tbl.table_schema
JOIN pg_catalog.pg_class pgc ON pgc.relname = tbl.table_name AND pgc.relnamespace=pgn.oid
JOIN pg_catalog.pg_description pgd_col ON pgd_col.objsubid = cols.ordinal_position AND pgd_col.objoid=pgc.oid
LEFT JOIN pg_catalog.pg_description pgd_tbl ON pgd_tbl.objsubid = 0 AND pgd_tbl.objoid=pgc.oid
WHERE tbl.table_schema='music' and tbl.table_name <> 'database_meta_data' 
ORDER BY tbl.table_schema, tbl.table_name, cols.column_name"""

# question="Which album contains the track title 'pull up' and which artist released it?"
# question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
# question="Show all album titles by recording artist Sizzla released on label Jet Star"
question="Can you show all album titles by artist Sizzla released on label Jet Star?"

try:
    start_time=strftime("%H:%M:%S", localtime())
    connection_string=os.environ.get('DATABASE_URL')
    engine = db.create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
    df=pd.read_sql(table_schema_query,engine)
    table_names=df["table_name"].unique()
    table_schema=df.to_markdown(tablefmt="grid", index=False)
    # print(table_schema)
    
    # sql_prompt=SqlPrompt()
    # prompt=sql_prompt.generate_prompt(context=table_schema, question=question)
    # instruction_model=InstructionModel()
    # sql_statement=instruction_model.generate_response(prompt=prompt)
    # print(sql_statement)

    sql:str ="""SELECT table_name, table_meta_data , (vector_embeddings <#> '{query_vector}') as cosine_similarity
FROM database_meta_data
ORDER BY cosine_similarity DESC
LIMIT 4;"""    

    embed_mode=EmbeddingModel()
    query_vector=embed_mode.embed(question)
    df=pd.read_sql_query(con=engine, sql=sql.format(query_vector=query_vector))
    columns=df.columns.to_list()
    data=list(itertools.chain.from_iterable([[item.split('\n') for item in row.split('\n') if item] for row in df["table_meta_data"].to_list()]))
    rows=[row.split(',') for row in list(itertools.chain.from_iterable(data))]
    df = pd.DataFrame(rows, columns=columns)
    table_schema=df.to_markdown(tablefmt="grid", index=False)
    print(table_schema)

    # df=pd.read_sql(sql_statement,engine)
    # context=df.to_markdown(tablefmt="grid", index=False)

    # end_time=strftime("%H:%M:%S", localtime())
    # print(f"Response: {start_time} to {end_time}")

    # print(context)

except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise error
    