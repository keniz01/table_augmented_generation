from time import localtime, strftime

from ContextRetrieverAgent import ContextRetrieverAgent
from LLMSQLGeneratorAgent import LLMSQLGeneratorAgent
from LLMTextSummeriserAgent import LLMTextSummeriserAgent
from SQLExecutorAgent import SQLExecutorAgent
from prompts.sql_prompt import SqlPrompt
from prompts.summarizer_prompt import SummarizerPrompt

# question="Which album titles have the track title 'Pull up' and which recording artist released each of them?"
# question="Which album title has the track title 'Pull up' and which recording artist released it?"
# question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
# question="Can you show all album titles by artist Sizzla released on label Jet Star?"
# question="How many albums are released by record label 'Jet star'?"
# question = "How many tracks are on album '2006 Ragga' and what is the album genre name?"
# question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
question="Which genres does artist 'Buju Banton' appear in?"

start_time=strftime("%H:%M:%S", localtime())
database_schema_context=ContextRetrieverAgent.from_question(question=question)

sql_prompt=SqlPrompt()
prompt=sql_prompt.generate_prompt(context=database_schema_context, question=question)
sql_generator=LLMSQLGeneratorAgent()
sql_statement=sql_generator.generate_sql(prompt=prompt)

sql_executor = SQLExecutorAgent()
sql_response_context=sql_executor.execute_sql(sql_statement)

summarizer_prompt=SummarizerPrompt()
prompt=summarizer_prompt.generate_prompt(context=sql_response_context, question=question)
llm_summeriser=LLMTextSummeriserAgent()
response=llm_summeriser.summerise_text(prompt=prompt)
end_time=strftime("%H:%M:%S", localtime())
print(f"Response: {start_time} to {end_time}")
print(response)