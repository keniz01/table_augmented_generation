import re

class SQLFormatHelper():

    def __init__(self, sql: str):
        self.sql=sql

    def __remove_spaces(self):
        self.sql=self.sql.strip()
        return self

    def __extract_from_back_ticks(self):
        match = re.search(r"```sql\n(.*?)\n```", self.sql, re.DOTALL)
        if match:
            self.sql = match.group(1).strip()
        return self
    
    def __remove_wild_cards(self):
        self.sql=self.sql.replace("%",'')
        return self
    
    def __replace_equals_with_ilike_in_where_clause(self):
        pattern = r"=\s*'([^']*)'"
        self.sql = re.sub(pattern, r"ILIKE '\1'", self.sql)       
        return self
    
    def __replace_equals_with_in_in_where_clause(self):
        self.sql = re.sub(r'=\s*\(\s*SELECT', 'IN (SELECT', self.sql, flags=re.IGNORECASE | re.DOTALL)
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

        print(f'SQL =========== {self.sql}')
        self.sql=self.__remove_spaces() \
            .__extract_from_back_ticks() \
            .__remove_wild_cards() \
            .__replace_equals_with_ilike_in_where_clause() \
            .__replace_equals_with_in_in_where_clause() \
            .sql
                    
        
        print(f'SQL =========== {self.sql}')
        if not self.__is_safe_select_query():
            raise Exception("Invalid SQL query: Only valid SELECT statements are allowed.")

        return self.sql
