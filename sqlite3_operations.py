'''this comment exists just to get rid of annoying warning'''
import sqlite3

class sqlite3_operations(object):
    '''some common SQL operations based on sqlite3'''

    def __init__(self, **kwargs):
        '''initialize the database connection'''
        if 'db' in kwargs:
            self.db = kwargs['db']
            self.mx_conn = sqlite3.connect(self.db)
            self.mx_cursor = self.mx_conn.cursor()
        else:
            raise ValueError("need arg db")
    def connect_db(self,**kwargs):
        '''connect db, initialize self.mx_conn and self.mx_cursor'''
        if 'db' in kwargs:
            self.db = kwargs['db']
        self.mx_conn = sqlite3.connect(self.db)
        self.mx_cursor = self.mx_conn.cursor()

    def get_tables(self):
        '''get all table names in current database'''
        self.mx_cursor.execute('select name from sqlite_master where type="table"')
        return list(map(lambda x : x[0] , self.mx_cursor.fetchall()))

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
        str_execute = 'create table {table_name} ({primary_key}, {items_str})'.format(table_name = str(table_name), primary_key = primary_key, items_str = items_str)
        print(str_execute)
        self.mx_cursor.execute(str_execute)


    def get_columns(self,table_name):
        '''return all columns of table'''
        columns_l = list(map(lambda x: x[0], self.mx_cursor.execute('select * from {table_name}'.format(table_name = table_name )).description))
        return columns_l

    def valid_columns(self, table_name, *columns):
        '''check if columns are valid or not in table '''
        table_columns = set(self.get_columns(table_name))
        columns = set(columns)
        diff_columns = columns - table_columns
        if diff_columns:
            raise ValueError(*diff_columns," do not exist in table ",table_name)
        return True


    def insert_item(self, table_name, **kwargs):
        '''insert items into the table
        kwargs used to indicate item names and values'''
        target_columns = kwargs.keys()
        target_values = kwargs.values()

        self.valid_columns(table_name, *target_columns)

        str_columns = ', '.join(map(lambda x: str(x), target_columns))
        str_values = ', '.join(map(lambda x: "'"+str(x)+"'", target_values))
        str_locator = ','.join(map(lambda x: '?', target_columns))
        str_table_name = "'"+table_name+"'"
        str_execute = "insert into {table_name} ({columns}) values ({values})".format(table_name = table_name , columns = str_columns, values = str_values)
        self.mx_cursor.execute(str_execute)

    def update_item(self, table_name, dict_set, dict_where):
        '''update item
        dict_set should be a dcitionary identifying target columns
        dict_where should be a dictionary identifying select condition'''
        if not isinstance(dict_set,dict) or not isinstance(dict_where,dict):
            raise ValueError("dict_set and dict_where should both be dictionary")
        if self.valid_columns(table_name,  *dict_set.keys()) and self.valid_columns(table_name, *dict_where.keys()):
            print(type(dict_set))
            print(type(dict_where))
            str_set = ', '.join(map(lambda k: k+" = '"+str(dict_set[k])+"'",dict_set))
            str_where = ' and '.join(map(lambda k: k+" = '"+str(dict_where[k])+"'",dict_where))
            str_execute = 'update {table_name} set {str_set} where {str_where}'.format(table_name = table_name, str_set = str_set, str_where = str_where)
            self.mx_cursor.execute(str_execute)

    def get_all_items_by_table(self,table_name):
        '''get all items of table identified'''
        self.mx_cursor.execute('select * from {table_name}'.format(table_name = table_name))
        return self.mx_cursor.fetchall()

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
    insert_items = {'class':'haha', 'parent':'gaga'}
    for table in my_tables:
        print(table)
    my_opts.insert_item('classes', **insert_items)
    print("get all item")
    all_items = my_opts.get_all_items_by_table('classes')
    my_opts.update_item('classes',{'class':'update'},{'parent':'gaga'})
    print("get all item")
    all_items = my_opts.get_all_items_by_table('classes')
    for item in all_items:
        print(item)

    # my_opts.delete_table("classes")
    # my_tables = my_opts.get_tables()
    # for table in my_tables:
        # print(table)
    my_opts.close_connection()
