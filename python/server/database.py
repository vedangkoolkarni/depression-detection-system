import mysql.connector
db_connection = mysql.connector.connect(host="localhost",user="root",passwd="mysql",auth_plugin='mysql_native_password')
print(db_connection)