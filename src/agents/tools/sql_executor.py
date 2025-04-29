from typing import List
import psycopg
from psycopg.rows import TupleRow
from src.database_utils import DatabaseUtils

class SQLExecutor:
    def __init__(self, db_utils: DatabaseUtils):
        self.__db_utils=db_utils

    def execute(self, sql:str) -> List[TupleRow]:
        try:
            rows=self.__db_utils.fetch_all_rows(sql)
            return rows
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise error
