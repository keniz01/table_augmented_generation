from time import localtime, strftime
from agents.table_schema_retriever_agent import TableSchemaRetrieverAgent
from agents.sql_generator_agent import SQLGeneratorAgent
from agents.text_summariser_agent import TextSummariserAgent
from agents.sql_executor_agent import SQLExecutorAgent
from database_utils import DatabaseUtils
from llm_models.instruction_model import InstructionModel
from llm_models.text_embedding_model import TextEmbeddingModel
from prompts.sql_prompt import SQLPrompt
from prompts.text_summariser_prompt import TextSummariserPrompt

llm_model=InstructionModel()
db_utils=DatabaseUtils()
text_embedding_model=TextEmbeddingModel()

def get_db_schema_context(question: str) -> list:
    table_schema_retriever_agent=TableSchemaRetrieverAgent(text_embedding_model, db_utils)
    table_schema=table_schema_retriever_agent.from_question(question=question)
    return table_schema

def get_sql_from_llm(db_schema_context: str, question: str) -> str:
    sql_prompt=SQLPrompt()
    prompt=sql_prompt.generate_prompt(context=db_schema_context, question=question)
    sql_generator=SQLGeneratorAgent(llm_model)
    return sql_generator.generate_sql(prompt=prompt)

def execute_sql(sql: str) -> str:
    sql_executor = SQLExecutorAgent(db_utils)
    return sql_executor.execute(sql)

def summarise_sql_result_text(sql_result_text: str, question: str) -> str:
    text_summary_prompt=TextSummariserPrompt()
    prompt=text_summary_prompt.generate_prompt(context=sql_result_text, question=question)
    text_summary_agent=TextSummariserAgent(llm_model)
    return text_summary_agent.summarise_text(prompt=prompt)

def run_agent(question: str) -> str:
    db_schema_context=get_db_schema_context(question)
    sql=get_sql_from_llm(db_schema_context, question)
    sql_result_text=execute_sql(sql)
    db_utils.close()
    summary_text=summarise_sql_result_text(sql_result_text, question)
    return summary_text

if __name__ == "__main__":
    question="Which album titles have the track title 'Pull up' and which recording artist released each of them?"
    # question="Which album title has the track title 'Pull up' and which recording artist released it?"
    # question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
    # question="Can you show all album titles by artist Sizzla released on label Jet Star?"
    # question="How many albums are released by record label 'Jet star'?"
    # question = "How many tracks are on album '2006 Ragga' and what is the album genre name?"
    # question='Show all track titles on the album Party Alliance Vol 3-Retail CD'
    # question="Which genres does artist 'Buju Banton' appear in?"

    start_time=strftime("%H:%M:%S", localtime())
    response=run_agent(question)
    end_time=strftime("%H:%M:%S", localtime())
    print(f"Response: {start_time} to {end_time}")
    print(response)