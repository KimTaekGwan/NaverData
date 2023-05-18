import sqlite3
import datetime
import pandas as pd

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')


class Updatae_DB:
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
    
    def init_db(self):
        with open('data/init.sql', 'r') as sql_file:
            sql_script = sql_file.read()
        self.cur.executescript(sql_script)
        self.conn.commit()
    
    def insert_datas(self, datas:list, table_name:str):
        cols = ', '.join(self._insert_table_col(table_name))
        self.cur.executemany(f"INSERT INTO table1({cols}) VALUES(?,?,?)", datas)
        pass
    
    def _insert_table_col(self, table_name:str):
        t_c = {
            'Crawling_Keywords':[],
            'Search_Shop':[],
            'Query_Keyword':[],
            'Search_Keyword':[],
            'Keywords_Top':[],
            'Data_Product':[],
            'Crawling_store':[],
            'Data_Reviews':[],
            'Data_Posts':[],
            'Keyword_Reviews':[],
            'Keyword_Posts':[]
        }
        return t_c[table_name]
    
    def select_sql(self, sql):
        df = pd.read_sql_query(sql, self.conn)
        return df

    def select_last(self, table_name):
        sql = f'SELECT * FROM {table_name} ORDER BY ROWID DESC LIMIT 1'
        k = self.cur.execute(sql)
        return k.fetchall[0]
    
    def _close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DB("ver_05014.db")