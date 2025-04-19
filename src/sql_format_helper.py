import re

class SQLFormatHelper():

    def __init__(self, sql: str):
        self.sql=sql

    def __remove_spaces(self):
        self.sql=self.sql.strip()
        return self

    def __remove_back_ticks(self):
        self.sql=self.sql.replace('```sql','').replace('```','')
        return self
    
    def __remove_wild_cards(self):
        self.sql=self.sql.replace("%",'')
        return self
    
    def __replace_equals_with_ilike(self):
        pattern = r"=\s*'([^']*)'"
        self.sql = re.sub(pattern, r" ILIKE '\1'", self.sql)       
        return self
    
    def format_sql(self) -> str:
        return self.__remove_spaces().__remove_back_ticks().__remove_wild_cards().__replace_equals_with_ilike().sql
