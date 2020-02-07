import mysql.connector
import json
from pwd import secret

# creating connection to the db
db_connection = mysql.connector.connect(
    host="localhost",
    database='test',
    user="nithin",
    password=secret
)


# creating database_cursor to perform SQL operation
cursor = db_connection.cursor()

# creating table if doesnt exist in db
query_1 = "CREATE TABLE IF NOT EXISTS prod_logs(sno INT PRIMARY KEY, ide INT, name TEXT, db_type TEXT,scenario TEXT,sql_str TEXT,result_str TEXT,exception TEXT, encoded_result TEXT)"
cursor.execute(query_1)

# reading json file
json_data = open('task.json').read()
json_obj = json.loads(json_data)

# inserting data to the table in the db
for i in json_obj:
    ide = i.get('id')
    name = i.get('name')
    db_type = i.get('db_type')
    scenario = i.get('scenario')
    sql_str = i.get('sql_str')
    result_str = i.get('result_str')
    exception = i.get('exception')
    encoded_result = i.get('encoded_result')
    sno = i.get('sno')
    cursor.execute("INSERT INTO prod_logs (ide, name,db_type,scenario,sql_str,result_str,exception,encoded_result,sno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (ide, name, db_type, scenario, sql_str, result_str, exception, encoded_result, sno))
    # comitting is important whenever changes are being made to the table
    db_connection.commit()

# closing the connection
db_connection.close()
