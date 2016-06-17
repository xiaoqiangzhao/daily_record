import os, sys
import itertools
from time import localtime, strftime
from sqlite3_operations import sqlite3_operations
class record(object):

    def __init__(self,**kwargs):
        '''PROJECTDIR is the directory where works are put
        DB should be put in PROJECTDIR/DB'''
        self.PROJECTDIR = os.path.dirname(os.path.realpath(__file__))
        self.DBDIR = os.path.join(self.PROJECTDIR, 'DB')
        self.DB = "daily_record.db"
        if "db" in kwargs:
            self.DB = kwargs['db']
        self.sql = sqlite3_operations(db = os.path.join(self.DBDIR,self.DB))
        self.primary_key = 'id integer primary key autoincrement'
        self.record_heads = ['begin tinytext', 'end tinytext', 'works tinytext', 'description tinytext', 'comments tinytext', 'severity integer']

    def add_page(self,**kwargs):
        '''use current date as default table name or can be identified by arg page_name = 'xxx', please keep page name style as daily_+strftime("%Y%m%d") '''
        page_name = 'daily_'+strftime("%Y%m%d")
        if 'page_name' in kwargs:
            page_name = kwargs['page_name']
        print(page_name)
        if page_name in self.sql.get_tables():
            raise ValueError(page_name," already exists, please delele first with self.delete_page")
        self.sql.create_table(page_name, self.primary_key, *self.record_heads)



if __name__ == '__main__':
    m_r = record()
    # m_r.add_page(page_name = "day20160614")
    m_r.add_page()
    for table in m_r.sql.get_tables():
        print(table)
        print(m_r.sql.get_columns(table))
        for item in m_r.sql.get_all_items_by_table(table):
            print(item)
    m_r.sql.close_connection()
    pass
