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
    
    def __is_safe_select_query(self):

        self.sql = self.sql.strip().lower()

        if not self.sql.startswith("select"):
            return False

        forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "create", "exec", "--"]

        for keyword in forbidden_keywords:
            if keyword in self.sql:
                return False

        return True

    def format_sql(self) -> str:

        if not self.__is_safe_select_query():
            raise Exception("Invalid SQL query: Only valid SELECT statements are allowed.")

        return self.__remove_spaces().__remove_back_ticks().__remove_wild_cards().__replace_equals_with_ilike().sql
