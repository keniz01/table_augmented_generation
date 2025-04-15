import re

class LLMSQLResponseFormatter():

    def __init__(self, sql_response: str):
        self.sql_response=sql_response

    def __remove_spaces(self):
        self.sql_response=self.sql_response.strip()
        return self

    def __remove_back_ticks(self):
        self.sql_response=self.sql_response.replace('```sql','').replace('```','')
        return self
    
    def __remove_wild_cards(self):
        self.sql_response=self.sql_response.replace("%",'')
        return self
    
    def __replace_equals_with_ilike(self):
        pattern = r"=\s*'([^']*)'"
        self.sql_response = re.sub(pattern, r" ILIKE '\1'", self.sql_response)       
        return self
    
    def format_sql_response(self) -> str:
        return self.__remove_spaces().__remove_back_ticks().__remove_wild_cards().__replace_equals_with_ilike().sql_response
