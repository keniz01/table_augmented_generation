import logging
from src.llm_models.instruction_model import InstructionModel
from src.sql_format_helper import SQLFormatHelper
from src.custom_logger import LoggerConfigurator

class SQLGenerator:
    log_config = LoggerConfigurator(name="Table Augmented Generation", log_level=logging.DEBUG)
    logger = log_config.get_logger()

    def __init__(self, llm_model: InstructionModel):
        self.__llm_model=llm_model

    def generate_sql(self, prompt:str):
        sql=self.__llm_model.get_response(prompt)
        self.logger.debug(f"Debugging sql: {sql}", feature="generate_sql()")
        formatter=SQLFormatHelper(sql)
        formatted_sql=formatter.format_sql()
        self.logger.debug(f"Debugging feature: {formatted_sql}", feature="generate_sql()")
        return formatted_sql
    
