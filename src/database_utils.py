import os
import psycopg
from psycopg.rows import dict_row, TupleRow

class DatabaseUtils:

    def __init__(self):
        connection_string=os.environ.get('DATABASE_URL')
        conn = psycopg.connect(conninfo=connection_string, row_factory=dict_row)
        self.__cursor=conn.cursor()
        self.__cursor.execute('SET SESSION search_path=music')

    def fetch_all_rows(self, sql: str) -> list[TupleRow]:
        try:          
            self.__cursor.execute(sql)
            rows = self.__cursor.fetchall() 
            return rows
        except (Exception, psycopg.DatabaseError) as error:
            print('ERROR: ',error)
            raise error
    
    def close(self):
        self.__cursor.close()