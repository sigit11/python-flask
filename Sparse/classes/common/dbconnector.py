import MySQLdb
import MySQLdb.cursors

class dbconnector(object):
    """description of class"""

    def __init__(self, source = None, username = None, password = None, dbname = None):
        self.source = source
        self.username = username
        self.password = password
        self.dbname = dbname

    def db_connect(self):
        """
        Create Database connection by using value that already defined on init function
        """
        try:
            dbcon = MySQLdb.connect(self.source, self.username, self.password, self.dbname)
            #print 'connected' 
            return dbcon
        except:
            #print 'not connected'
            return 'error'

    def db_select_all(self, dbCon, table, condition = '', fetch = 'all'):
        """
        Select all data from all columns of a table by using these arguments:
        dbCon = Database Connection
        table = String of table name
        condition = string of additional condition inside the query 
        fetch = all / one (all : for all available rows, one : one row only)
        """
        try:
            db = dbCon
            cursor = dbCon.cursor()
            query = "SELECT * FROM " + str(table) + " " + str(condition)
            cursor.execute(query)
            if fetch == 'all':
                data = cursor.fetchall()
            elif fetch == 'one':
                data = cursor.fetchone()
            return {'status' : 'Success', 'data' : data}
        except:
            #print cursor._last_executed
            return {'status' : 'error'}

    def db_select_columns(self, dbCon, columns = [] , table = str, condition = '', fetch = 'all'):
        """
        Select data from specific columns of a table by using these arguments:
        dbCon = Database Connection
        columns = Array of columns
        table = String of table name
        condition = string of additional condition inside the query 
        fetch = all / one (all : for all available rows, one : one row only)
        """
        try:
            print("ada")
            db = dbCon
            cursor = dbCon.cursor()
            columnString = ",".join(str(column) for column in columns)
            query = "SELECT " + columnString + " FROM " + str(table) + " " + str(condition)
            print(query)
            cursor.execute(query)
            if fetch == 'all':
                data = cursor.fetchall()
            elif fetch == 'one':
                data = cursor.fetchone()
            return {'status' : 'Success', 'data' : data}
        except:
            #print cursor._last_executed
            return {'status' : 'error'}

    def db_insert(self, dbCon, table, columns = [], values = {}, condition = ''):
        """
        Inserting into database table by using these arguments:
        dbCon = Database Connection
        table = table name
        columns = Array of columns
        values = Dict of value with the same name of columns name on the key part of the Dict
        condition = string of additional condition inside the query 
        """
        try:
            db = dbCon
            cursor = dbCon.cursor()
            columnString = ",".join(str(column) for column in columns)
            valueString = ",".join(" %(" + str(value) + ")s" for value in columns)
            query = "INSERT INTO " + str(table) + " ( " + columnString + " ) VALUES ( " + valueString + " ) " + condition
            #print query
            cursor.execute(query, values)
            lastid = cursor.lastrowid
            db.commit()
            return {'status' : 'Success', 'lastid' : lastid}
        except:
            print(cursor._last_executed)
            db.rollback()
            return {'status' : 'error'}

    def db_insert_multiple(self, dbCon, table, columns = [], values = [], condition =''):
        """
        Inserting multiple row into database table by using these arguments:
        dbCon = Database Connection
        columns = Array of columns
        values = array of value tuple for every row
        condition = string of additional condition inside the query 
        """
        try:
            db = dbCon
            cursor = dbCon.cursor()
            columnString = ",".join(str(column) for column in columns)
            valueString = ", ".join("%s" for column in range(0, len(columns)))
            query = "INSERT INTO " + str(table) + " ( " + columnString + " ) VALUES ( " + valueString + " ) " + condition
            #print query
            cursor.executemany(query, values)
            db.commit()
            return {'status' : 'Success'}
        except:
            #print cursor._last_executed
            db.rollback()
            return {'status' : 'error'}

    def db_insert_multiple_dicto(self, dbCon, table, columns = [], values = [], condition =''):
        """
        Inserting multiple row into database table by using these arguments:
        dbCon = Database Connection
        columns = Array of columns
        values = array of value tuple for every row
        condition = string of additional condition inside the query 
        """
        try:
            print("ada")
            db = dbCon
            cursor = dbCon.cursor()
            columnString = ",".join(str(column) for column in columns)
            valueString = ", ".join("%(" + column + ")s" for column in columns)
            query = "INSERT INTO " + str(table) + " ( " + columnString + " ) VALUES ( " + valueString + " ) " + condition
            print(query)
            cursor.executemany(query, values)
            db.commit()
            return {'status' : 'Success'}
        except:
            #print cursor._last_executed
            db.rollback()
            return {'status' : 'error'}

    def db_update(self, dbCon, table, set = {}, condition = ''):
        """
        Inserting into database table by using these arguments:
        dbCon = Database Connection
        table = Table name
        set = Dict of value with the same name of columns name on the key part of the Dict
        condition = string of additional condition inside the query 
        """
        try:
            db = dbCon
            cursor = dbCon.cursor()
            setString = ",".join(str(key) + " = %(" + str(key) + ")s" for key, value in set.items())
            query = "UPDATE " + str(table) + " SET " + setString + " " + condition
            print(query)
            cursor.execute(query, set)
            lastid = cursor.lastrowid
            db.commit()
            return {'status' : 'Success', 'lastid' : lastid}
        except Exception as e:
            print(e)
            print(cursor._last_executed)
            db.rollback()
            return {'status' : 'error'}

    def db_custom_query(self, dbCon, query, values, fetch = 'all'):
        """
        Create custom query by using these parameters:
        dbCon = Database Connection
        query = custom query to execute
        value = any values format to process along with the query. It can be a list of touple or dictionary
        fetch = all / one (all : for all available rows, one : one row only)
        """
        try:
            db = dbCon
            cursor = dbCon.cursor()
            cursor.execute(query, values)
            if fetch == 'all':
                data = cursor.fetchall()
            elif fetch == 'one':
                data = cursor.fetchone()
            return {'status' : 'Success', 'data' : data}
        except:
            print(cursor._last_executed)
            return {'status' : 'error'}



