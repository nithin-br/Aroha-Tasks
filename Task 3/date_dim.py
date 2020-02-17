# importing the necessary modules
import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, CHAR, VARCHAR
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=Warning)
import holidays

# database credentials accessed as environment variables
host = os.environ.get('db_local_host')
user = os.environ.get('db_local_user')
password = os.environ.get('db_local_pwd')
database = 'test0'

# establishing connection to the MySQL database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(host=host, user=user, pw=password, db=database))

# Declarative base for sqlalchemy required to create table
Base = declarative_base()

# Creating the table along with the fields,specified datatypes and widths as per scenario using sqlalchemys base class


class Date_Dim(Base):

    __tablename__ = 'DATE_DIM'
    DATEKEY = Column(Integer, primary_key=True)
    THEDATE = Column(DateTime)
    YEAR = Column(Numeric)
    MONTH = Column(Numeric)
    YEARMONTH = Column(CHAR(7))
    MONTHNAME = Column(VARCHAR(9))
    MONTHABBR = Column(VARCHAR(3))
    DAY = Column(Numeric)
    DAYOFWEEK = Column(Numeric)
    DAYOFWEEKNAME = Column(VARCHAR(9))
    DAYOFWEEKABBR = Column(VARCHAR(3))
    QUARTER = Column(Numeric)
    SEASON = Column(VARCHAR(6))
    HOLIDAY = Column(VARCHAR(30))
    CURRENTYEAR = Column(CHAR(4))
    PRIORYEAR = Column(CHAR(4))
    CURRENTMONTH = Column(CHAR(2))
    PRIORMONTH = Column(CHAR(2))
    FIRSTOFMONTH = Column(CHAR(1))
    BUSINESSDAY = Column(CHAR(1))
    FISCALMONTH = Column(VARCHAR(20))

# creating table
# Date_Dim.__table__.create(engine)

# reading table from mysql db


# making connection
dbConnection = engine.connect()
data = pd.read_sql("select * from test0.date_dim", dbConnection, parse_dates=['THEDATE'])

# closing the connection
dbConnection.close()

'''Function which takes in one input parameter:
1. year as string in the format yyyy
checks for the condition (leap year or not) and then populates the table based on the fields as per the scenario
returns the populated table'''


def populate_date_dim(year):
    # Leap Year Check and assign value for the periods accordingly
    if (int(year) % 4) == 0:
        if (int(year) % 100) == 0:
            if (int(year) % 400) == 0:
                data['THEDATE'] = pd.date_range(start='01/01/' + year, periods=366)
            else:
                data['THEDATE'] = pd.date_range(start='01/01/' + year, periods=365)
        else:
            data['THEDATE'] = pd.date_range(start='01/01/' + year, periods=366)
    else:
        data['THEDATE'] = pd.date_range(start='01/01/' + year, periods=365)

    uk_holidays = holidays.UnitedKingdom()
    for index, val in enumerate(data.THEDATE):
        data['DATEKEY'].loc[index] = int(str(val.date()).replace('-', ''))
        data['YEAR'].loc[index] = val.year
        data['CURRENTYEAR'].loc[index] = str(val.year)
        data['PRIORYEAR'].loc[index] = str((val.year) - 1)
        data['YEARMONTH'].loc[index] = val.to_period('M')
        data['MONTH'].loc[index] = val.month
        data['CURRENTMONTH'].loc[index] = str(val.month)
        data['MONTHNAME'].loc[index] = val.month_name()
        data['MONTHABBR'].loc[index] = val.month_name()[0:3]
        data['DAY'].loc[index] = val.day
        data['DAYOFWEEK'].loc[index] = val.dayofweek + 1
        data['DAYOFWEEKNAME'].loc[index] = val.day_name()
        data['DAYOFWEEKABBR'].loc[index] = val.day_name()[0:3]
        data['QUARTER'].loc[index] = val.quarter

        # prior month (if current month is january then display a msg)
        if data['MONTHABBR'].loc[index] == 'Jan':
            data['PRIORMONTH'].loc[index] = '12'
        else:
            data['PRIORMONTH'].loc[index] = str((val.month) - 1)

        # season
        if data['MONTHABBR'].loc[index] in ('Apr', 'May', 'Jun'):
            data['SEASON'].loc[index] = 'Summer'
        elif data['MONTHABBR'].loc[index] in ('Oct', 'Nov', 'Dec', 'Jan'):
            data['SEASON'].loc[index] = 'Winter'
        elif data['MONTHABBR'].loc[index] in ('Jul', 'Aug', 'Sep'):
            data['SEASON'].loc[index] = 'Monsoon'
        elif data['MONTHABBR'].loc[index] in ('Feb', 'Mar'):
            data['SEASON'].loc[index] = 'Spring'

        # Holidays: considering holidays for UK. the holidays module has various other countries as well
        if (val in uk_holidays):
            data['HOLIDAY'].loc[index] = uk_holidays.get(val)
        elif data['DAYOFWEEKABBR'].loc[index] in ('Sat', 'Sun'):
            data['HOLIDAY'].loc[index] = 'Weekend'
        else:
            data['HOLIDAY'].loc[index] = 'No Holiday'

        # bussiness day (if holiday then 0 and if no holiday then 1)
        if (data['HOLIDAY'].loc[index] == 'No Holiday'):
            data['BUSINESSDAY'].loc[index] = '1'
        else:
            data['BUSINESSDAY'].loc[index] = '0'

        # first of month (if day in the date is 01 then set firstofmonth flag to true (1) or esle False (0) )
        if (data['DAY'].loc[index] == 1.0):
            data['FIRSTOFMONTH'].loc[index] = '1'
        else:
            data['FIRSTOFMONTH'].loc[index] = '0'

        '''fiscal month considering that the fiscal year starts from 01-apr-2020'''

        if data['MONTHABBR'].loc[index] == 'Apr':
            data['FISCALMONTH'].loc[index] = 'One'
        elif data['MONTHABBR'].loc[index] == 'May':
            data['FISCALMONTH'].loc[index] = 'Two'
        elif data['MONTHABBR'].loc[index] == 'Jun':
            data['FISCALMONTH'].loc[index] = 'Three'
        elif data['MONTHABBR'].loc[index] == 'Jul':
            data['FISCALMONTH'].loc[index] = 'Four'
        elif data['MONTHABBR'].loc[index] == 'Aug':
            data['FISCALMONTH'].loc[index] = 'Five'
        elif data['MONTHABBR'].loc[index] == 'Sep':
            data['FISCALMONTH'].loc[index] = 'Six'
        elif data['MONTHABBR'].loc[index] == 'Oct':
            data['FISCALMONTH'].loc[index] = 'Seven'
        elif data['MONTHABBR'].loc[index] == 'Nov':
            data['FISCALMONTH'].loc[index] = 'Eight'
        elif data['MONTHABBR'].loc[index] == 'Dec':
            data['FISCALMONTH'].loc[index] = 'Nine'
        elif data['MONTHABBR'].loc[index] == 'Jan':
            data['FISCALMONTH'].loc[index] = '10th fiscal month of 2019'
        elif data['MONTHABBR'].loc[index] == 'Feb':
            data['FISCALMONTH'].loc[index] = '11th fiscal month of 2019'
        elif data['MONTHABBR'].loc[index] == 'Mar':
            data['FISCALMONTH'].loc[index] = '12th fiscal month of 2019'
    return data


# calling the function
data = populate_date_dim('2020')

# converting the dataframe to a .csv file
data.to_csv('date_dim.csv', index=False)
