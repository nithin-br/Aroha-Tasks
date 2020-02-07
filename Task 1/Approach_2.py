# importing the necessary modules
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from pwd import secret

'''user defined function which takes in the input parameters (json_file_name and the db server credentials along with 
the database name to which one wants to connect) and returns a table created in the rspective MySQL db'''


def json_to_mysql(json_file_name, host, user, password, database):
    # creating connection to the db
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=host, user=user, pw=password, db=database))

    # reading the json file using pandas. this converts the json file to pandas dataframe
    data = pd.read_json(json_file_name)

    # getting table name from the file name
    l = json_file_name.split('.')
    table_name = l[0]

    # adding the dataframe to the connected mysql table.
    return (data.to_sql(con=engine, name=table_name, if_exists='replace'))


# calling the function
json_to_mysql('task.json', 'localhost', 'nithin', secret, 'test')
