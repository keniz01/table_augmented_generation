import os
import re
from time import localtime, strftime
import psycopg
from psycopg.rows import dict_row
import pandas as pd
import sqlalchemy as db
from language_models import InstructionModel
from summarizer_prompt import SummarizerPrompt
from sql_prompt import SqlPrompt
from database_context_retriever import DatabaseContextRetriever

def replace_equals_with_ilike(sql_query):
    pattern = r"=\s*'([^']*)'"
    modified_query = re.sub(pattern, r" ILIKE '\1'", sql_query)
    return modified_query

# question="Which album titles have the track title 'Pull up' and which recording artist released each of them?"
# question="Which album title has the track title 'Pull up' and which recording artist released it?"
# question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
# question="Can you show all album titles by artist Sizzla released on label Jet Star?"
# question="How many albums are released by record label 'Jet star'?"
# question = "How many tracks are on album '2006 Ragga' and what is the album genre name?"
# question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
# question="Can you show all album titles by artist Sizzla released on label Jet Star?"
question="Which genres does artist 'Buju Banton' appear in?"

start_time=strftime("%H:%M:%S", localtime())
database_schema_context=DatabaseContextRetriever.from_question(question=question)

sql_prompt=SqlPrompt()
prompt=sql_prompt.generate_prompt(context=database_schema_context, question=question)
instruction_model=InstructionModel()
sql_statement=instruction_model.generate_sql_response(prompt=prompt)

try:
    connection_string=os.environ.get('DATABASE_URL')
    # engine = db.create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
    # df=pd.read_sql(sql_statement,engine)
    # context=df.to_markdown(tablefmt="grid", index=False)
    conn = psycopg.connect(conninfo=connection_string, row_factory=dict_row)
    cursor = conn.cursor()
    cursor.execute('SET SESSION search_path=music') 
    modified_sql = replace_equals_with_ilike(sql_statement)
    cursor.execute(modified_sql)
    sql_response_context = cursor.fetchall()  
except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise error

summarizer_prompt=SummarizerPrompt()
prompt=summarizer_prompt.generate_prompt(context=sql_response_context, question=question)
response=instruction_model.generate_summary_response(prompt=prompt)
end_time=strftime("%H:%M:%S", localtime())
print(f"Response: {start_time} to {end_time}")
print(response)