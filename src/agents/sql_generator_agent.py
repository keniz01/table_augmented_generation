from llm_models.instruction_model import InstructionModel
from sql_format_helper import SQLFormatHelper

class SQLGeneratorAgent():
    
    def __init__(self, llm_model: InstructionModel):
        self.__llm_model=llm_model

    def generate_sql(self, prompt:str):
        sql_text=self.__llm_model.get_response(prompt)
        formatter=SQLFormatHelper(sql_text)
        return formatter.format_sql()
