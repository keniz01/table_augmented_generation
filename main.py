import os
from time import localtime, strftime
import psycopg
import pandas as pd
import sqlalchemy as db
from response_prompt import ResponseSynthesizePrompt
from sql_prompt import SqlPrompt

# question="Which album contains the track 'pull up' and which artist released it?"
# question='List all tracks on the album Party Alliance Vol 3-Retail CD'
sql_prompt=SqlPrompt()
question="Can you show all album titles by artist Mavado release on label Jet Star?"
start_time=strftime("%H:%M:%S", localtime())
sql_statement=sql_prompt.generate_response(question=question)
print(sql_statement)

try:
    connection_string=os.environ.get('DATABASE_URL')
    engine = db.create_engine(connection_string, connect_args={'options': '-csearch_path=music'})
    df=pd.read_sql(sql_statement,engine)
    context=df.to_json(orient="records" ,index=False)
except (Exception, psycopg.DatabaseError) as error:
	print('ERROR: ',error)
	raise error

prompt=ResponseSynthesizePrompt()
response=prompt.generate_response(context=context)
end_time=strftime("%H:%M:%S", localtime())
print(f"Response: {start_time} to {end_time}")
print(response)