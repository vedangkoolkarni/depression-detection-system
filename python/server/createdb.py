import mysql.connector
db_connection = mysql.connector.connect(
    host="localhost", user="root", passwd="mysql", database="depression_detection_system")
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor(buffered=True)
# executing cursor with execute method and pass SQL query
# db_cursor.execute("CREATE DATABASE depression_detection_system")
# db_cursor.execute("CREATE TABLE  user(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255),phone_no VARCHAR(30),password VARCHAR(30))")
# print("Table Created Successfully")
# get list of all databases
# db_cursor.execute("SHOW DATABASES")
# Get database table
# db_cursor.execute("SHOW TABLES")
# print all databases
# for db in db_cursor:
#     print(db)


def insert_user(name, email, phone_no, password):
    return_val = ''
    try:
        sql = "select * from user where email = %s"
        val = (email,)
        db_cursor.execute(sql, val)
        my_result = db_cursor.fetchone()

        if my_result:
            return_val = 'already-exists'
        else:
            try:
                sql = "INSERT INTO user (name, email, phone_no, password) VALUES (%s, %s, %s, %s)"
                val = (name, email, phone_no, password)
                db_cursor.execute(sql, val)
                db_connection.commit()
                print(db_cursor.rowcount, "record inserted.")
                return_val = 'success'
            except Exception as e:
                print('error : ', e)
                return_val = 'error'
    except Exception as e:
        print('Invalid Credentials', e)
        return_val = 'error'
    return return_val
    

def login_user(email, password):
    return_val = ''
    print('email to login', email)
    print('email to password', password)
    try:
        sql = "select * from user where email = %s and password = %s"
        val = (email, password)
        db_cursor.execute(sql, val)
        my_result = db_cursor.fetchone()

        if my_result:
            return_val = 'success'
        else:
            return_val = 'failure'
        print('value to return is ', return_val)
    except Exception as e:
        return_val = 'error'
        print('something wrong', e)
    return return_val