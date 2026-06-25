import pymysql

def db_connection():
    connection=pymysql.connect(
        host="localhost",
        user="root",
        password="#Rittik123",
        database="task_manager",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection