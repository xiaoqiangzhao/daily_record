#! /home/b51816/local/bin/python3
import os, sys
import itertools
from time import localtime, strftime
import sqlite3
import sqlite3_opts
class record(object):

    def __init__(self,**kwargs):
        self.PROJECTDIR = os.path.dirname(os.path.realpath(__file__))
        self.DB = "daily_record.db"
        if kwargs['db']:
            self.DB = kwargs['db']
        self.sql_opts = sqlite3_operations(self.DB)



if __name__ == '__main__':
    my_record = record(db='jay_record.db')
    print("PROJECTDIR",my_record.PROJECTDIR,sep="==>")
    print("DB",my_record.DB,sep="==>")
    tables = my_record.get_all_tables(my_record.DB)
    if not tables:
        print("no tables found")
    else:
        for table in tables:
            print("=>  ",table)

