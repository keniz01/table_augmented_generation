import os
from time import localtime, strftime
import psycopg
import pandas as pd
import sqlalchemy as db
from language_models import InstructionModel
from summarizer_prompt import SummarizerPrompt
from sql_prompt import SqlPrompt
from database_context_retriever import DatabaseContextRetriever

# question="Which album contains the track title 'Pull up' and which artist released it?"
question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
# question="Can you show all album titles by artist Sizzla released on label Jet Star?"
start_time=strftime("%H:%M:%S", localtime())
context=DatabaseContextRetriever.from_question(question=question)

sql_prompt=SqlPrompt()
prompt=sql_prompt.generate_prompt(context=context, question=question)
instruction_model=InstructionModel()
sql_statement=instruction_model.generate_response(prompt=prompt)
print(sql_statement)
try:
    connection_string=os.environ.get('DATABASE_URL')
    engine = db.create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
    df=pd.read_sql(sql_statement,engine)
    context=df.to_markdown(tablefmt="grid", index=False)
except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise error

summarizer_prompt=SummarizerPrompt()
prompt=summarizer_prompt.generate_prompt(context=context, question=question)
print(prompt)
response=instruction_model.generate_response(prompt=prompt)
end_time=strftime("%H:%M:%S", localtime())
print(f"Response: {start_time} to {end_time}")
print(response)