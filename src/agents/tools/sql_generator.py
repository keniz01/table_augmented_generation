from llm_models.instruction_model import InstructionModel
from sql_format_helper import SQLFormatHelper

class SQLGenerator:
    
    def __init__(self, llm_model: InstructionModel):
        self.__llm_model=llm_model

    def generate_sql(self, prompt:str):
        sql=self.__llm_model.get_response(prompt)
        formatter=SQLFormatHelper(sql)
        formatted_sql=formatter.format_sql()
        return formatted_sql
    
