#! /home/b51816/local/bin/python3
'''this comment exists just to get rid of annoying warning'''
import sqlite3

class sqlite3_operations(object):
    '''some common SQL operations based on sqlite3'''

    def __init__(self, **kwargs):
        '''initialize the database connection'''
        if kwargs['db']:
            self.db = kwargs['db']
            self.mx_conn = sqlite3.connect(self.db)
            self.mx_cursor = self.mx_conn.cursor()
        else:
            raise ValueError("need arg db")

    def get_tables(self):
        '''get all table names in current database'''
        self.mx_cursor.execute('select name from sqlite_master where type="table"')
        return self.mx_cursor.fetchall()

    def IsTableExist(self, table_name):
        '''check if the table_name exists in current database'''
        self.mx_cursor.execute('select name from sqlite_master where type="table" and name = ?',(table_name,))
        table= self.mx_cursor.fetchall()
        if table:
            return True
        else:
            return False

    def delete_table(self, table_name):
        '''delete table in current database
        return True if table exists and deleted successfully
        return False if table doesn't exist '''
        if self.IsTableExist(table_name):
            self.mx_cursor.execute('drop table %s' % table_name)
            print("table",table_name,"deleted",sep=" ")
            return True
        else:
            return False

    def create_table(self,table_name, primary_key, *args):
        '''create table
        primary_key for primary key in the table
        args identify the items and item size'''
        if self.IsTableExist(table_name):
           print("table %s already exist, delete and re-generate" % table_name)
           self.mx_cursor.execute('drop table %s'% table_name)
        items_str = ", ".join(args)
        self.mx_cursor.execute('create table {table_name} ({primary_key}, {items_str})'.format(table_name = table_name, primary_key = primary_key, items_str = items_str))

    def get_columns(self,table_name):
        '''return all columns of table'''
        columns_l = list(map(lambda x: x[0], self.mx_cursor.execute('select * from {table_name}'.format(table_name = table_name )).description))
        print(columns_l)
        return columns_l

    def insert_item(self, table_name, **kwargs):
        '''insert items into the table
        kwargs used to indicate item names and values'''
        table_columns = set(self.get_columns(table_name))
        target_columns = kwargs.keys()
        diff_columns = target_columns - table_columns
        if diff_columns:
            raise ValueError(*diff_columns," do not exist in table ",table_name)
        target_values = kwargs.values()

    def close_connection(self):
        '''close the database connection'''
        self.mx_cursor.close()
        self.mx_conn.commit()
        self.mx_conn.close()

if __name__ == '__main__':
    my_opts = sqlite3_operations(db='test.db')
    items = ['class tinytext', 'parent tinytext', 'function text', 'task text']
    my_opts.create_table('classes','id integer primary key autoincrement',*items)
    l = my_opts.get_columns("classes")
    my_tables = my_opts.get_tables()
    insert_items = {'class':'haha', 'parent':'gaga', 'dodo':'no','peipei':'yes'}
    for table in my_tables:
        print(table)
    my_opts.insert_item('classes', **insert_items)
    my_opts.delete_table("classes")
    my_tables = my_opts.get_tables()
    for table in my_tables:
        print(table)
    my_opts.close_connection()
