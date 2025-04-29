
from typing import Dict, List
from agents.tools.sql_executor import SQLExecutor
from agents.tools.sql_generator import SQLGenerator
from agents.tools.table_schema_retriever import TableSchemaRetriever
from agents.tools.text_summariser import TextSummariser
from database_utils import DatabaseUtils
from llm_models.embedding_model import EmbeddingModel
from llm_models.instruction_model import InstructionModel
from prompts.sql_prompt import SQLPrompt
from prompts.text_summariser_prompt import TextSummariserPrompt


class DatabaseAgent:
    def __init__(self, llm_model: InstructionModel, embedding_model: EmbeddingModel, db_utils: DatabaseUtils):        
        self.__llm_model=llm_model
        self.__embedding_model=embedding_model
        self.__db_utils=db_utils

    def __get_db_schema(self, question: str) -> List[Dict]:
        table_schema_retriever_agent=TableSchemaRetriever(self.__embedding_model, self.__db_utils)
        table_schema=table_schema_retriever_agent.from_question(question=question)
        return table_schema

    def __generate_sql_from_llm(self, db_schema: str, question: str) -> str:
        sql_prompt=SQLPrompt()
        prompt=sql_prompt.generate_prompt(context=db_schema, question=question)
        sql_generator=SQLGenerator(self.__llm_model)
        return sql_generator.generate_sql(prompt=prompt)

    def __execute_sql(self, sql: str) -> str:
        sql_executor = SQLExecutor(self.__db_utils)
        return sql_executor.execute(sql)

    def __summarise_text(self, sql_result_text: str, question: str) -> str:
        text_summary_prompt=TextSummariserPrompt()
        prompt=text_summary_prompt.generate_prompt(context=sql_result_text, question=question)
        text_summariser=TextSummariser(self.__llm_model)
        return text_summariser.summarise_text(prompt=prompt)

    def invoke(self, question: str) -> str:
        db_schema=self.__get_db_schema(question)
        sql=self.__generate_sql_from_llm(db_schema, question)
        sql_result=self.__execute_sql(sql)
        summary_text=self.__summarise_text(sql_result, question)
        return summary_text
