# importing the necessary modules
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from pwd import secret

# creating connection to the db
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host="localhost", user="nithin", pw=secret, db="test"))

# reading the json file using pandas. this converts the json file to pandas dataframe
data = pd.read_json('task.json')
table_name = "log"
# adding the dataframe to the connected mysql table.
data.to_sql(con=engine, name=table_name, if_exists='replace')
